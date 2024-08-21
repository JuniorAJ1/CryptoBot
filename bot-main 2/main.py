import discord
import asyncio
import os
import time
import mplfinance as mpf
from discord.ext import commands
from dotenv import load_dotenv
from Indicators.indic import calculate_ema
from Data.data_collection import get_realtime_data, get_latest_price
from patterns.mainPatterns.signal_generator import SignalGenerator
from functools import lru_cache

# Load environment variables from the .env file
load_dotenv()

# Get Binance API keys and Discord token from environment variables
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
discord_token = os.getenv('DISCORD_TOKEN')

# Check if all required environment variables are set
if not api_key or not api_secret or not discord_token:
    raise ValueError("One or more environment variables are missing.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Cache the latest price to reduce frequent API calls
@lru_cache(maxsize=10)
def get_cached_latest_price(symbol):
    return get_latest_price(symbol)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='signal')
async def single_signal(ctx, symbol: str, interval: str):
    signal_generator = SignalGenerator(symbol, interval)
    try:
        live_price, current_data = await asyncio.gather(
            asyncio.to_thread(get_cached_latest_price, symbol),
            asyncio.to_thread(get_realtime_data, symbol, interval)
        )

        signals, _ = signal_generator.generate_signals(current_data, generate_plot=False)  # Unpack the tuple

        if signals:
            response = "\n".join([f"{signal.split('Price at')[0].strip()} Live Price: {live_price}" for signal in signals])
        else:
            response = "No signals found."

        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error generating signals: {e}")

@bot.command(name='control')
async def control_signal(ctx, symbol: str, interval: str, time_limit: str, duration: str):
    timeout = time.time() + 60 * float(time_limit)
    signal_generator = SignalGenerator(symbol, interval)

    while True:
        if time.time() > timeout:
            await ctx.send("Time has elapsed for updates")
            break

        try:
            live_price, current_data = await asyncio.gather(
                asyncio.to_thread(get_cached_latest_price, symbol),
                asyncio.to_thread(get_realtime_data, symbol, interval)
            )

            signals, _ = signal_generator.generate_signals(current_data, generate_plot=False)  # Unpack the tuple

            if signals:
                response = "\n".join([f"{signal.split('Price at')[0].strip()} Live Price: {live_price}" for signal in signals])
            else:
                response = "No signals found."

            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error generating signals: {e}")

        await asyncio.sleep(int(duration))  # Pause between updates

@bot.command(name='timer')
async def timer_signal(ctx, symbol: str, interval: str, time_limit: str):
    timeout = time.time() + 60 * float(time_limit)
    signal_generator = SignalGenerator(symbol, interval)

    while True:
        if time.time() > timeout:
            await ctx.send("Time has elapsed for updates")
            break

        try:
            live_price, current_data = await asyncio.gather(
                asyncio.to_thread(get_cached_latest_price, symbol),
                asyncio.to_thread(get_realtime_data, symbol, interval)
            )

            signals, _ = signal_generator.generate_signals(current_data, generate_plot=False)  # Unpack the tuple

            if signals:
                response = "\n".join([f"{signal.split('Price at')[0].strip()} Live Price: {live_price}" for signal in signals])
            else:
                response = "No signals found."

            await ctx.send(response)
        except Exception as e:
            await ctx.send(f"Error generating signals: {e}")

        await asyncio.sleep(10)  # Update every 10 seconds


@bot.command(name='generate')
async def generate_graph(ctx, symbol: str, interval: str):
    signal_generator = SignalGenerator(symbol, interval)
    try:
        # Fetch real-time data in a separate thread
        current_data = await asyncio.to_thread(get_realtime_data, symbol, interval)

        if 'EMA50' not in current_data.columns:
            current_data['EMA50'] = calculate_ema(current_data)

        signals, plot_filename = signal_generator.generate_signals(current_data, generate_plot=True)
        response = "Signals generated.\n" + "\n".join(signals)
        await ctx.send(response)

        # Check if a plot was generated and send it
        if plot_filename and os.path.exists(plot_filename):
            await ctx.send(file=discord.File(plot_filename))
            os.remove(plot_filename)  # Delete the file after sending
        else:
            await ctx.send("No pattern detected or unable to generate plot.")
    except Exception as e:
        await ctx.send(f"Error generating graph: {e}")

# Run the bot using the Discord token
bot.run(discord_token)
