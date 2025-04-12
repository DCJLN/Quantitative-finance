import yfinance as yf
import telegram
import asyncio
from invest_bot import InvestBot


# noinspection PyMethodMayBeStatic
def send_telegram_alert(msg, fig):
    """
    Function that manages message sending to telegram channel.
    @param msg: the message to send.
    @param fig: the plotly figure to send.
    @return: None
    """
    fig.write_image('fig_to_send.png', engine='orca')

    bot_token = "7191274095:AAHWT5vXJ2owAZXptfxfsXy5hBTsb2AKIMY"
    chat_id = 7162781343
    bot = telegram.Bot(token=bot_token)

    async def send():
        await bot.send_photo(chat_id=chat_id, photo=open('fig_to_send.png', 'rb'), caption=msg)

    try:
        asyncio.run(send())
    except RuntimeError:
        # In case there's already an event loop running (e.g., Jupyter)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send())

    print("=> Alert sent.")


def main():
    # Parameters
    HIST_PERIOD = '1y'
    INTERVAL = '1d'
    TICKER = "^GSPC"

    # Downloading financial data
    sp_500_data = yf.download(tickers=TICKER,
                              period=HIST_PERIOD,
                              interval=INTERVAL,
                              auto_adjust=False,
                              multi_level_index=False)

    # Cleaning and formatting data
    sp_500_data = sp_500_data.ffill()
    sp_500_data.dropna(inplace=True)

    # Creating the investment bot
    inv_bot = InvestBot(fin_data=sp_500_data)

    # Applying the strategy
    bb_out_up_signals, bb_out_up_fig = inv_bot.bb_out_up_strategy(parameters=None, graph_length=50)

    if bb_out_up_signals['signal'].iloc[-1]:
        msg = f'New signal from bb_out_up strategy:\n'
        msg += f'\t -> {TICKER} value: {round(sp_500_data["Adj Close"].iloc[-1], 2)}'
        send_telegram_alert(msg, bb_out_up_fig)


if __name__ == '__main__':
    main()
