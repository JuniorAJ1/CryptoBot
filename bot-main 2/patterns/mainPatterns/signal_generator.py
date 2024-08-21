import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from Data.data_collection import get_realtime_data
from patterns.mainPatterns.double_patterns import detect_double_top, detect_double_bottom
from patterns.mainPatterns.triple_patterns import detect_triple_top, detect_triple_bottom
from patterns.headShoulder.head_shoulder import detect_head_and_shoulders, detect_inverse_head_and_shoulders, detect_early_aggressive_entry
from patterns.trendChange.trend_change import detect_trend_change_bullish, detect_trend_change_bearish
from patterns.trendContinuation.trend_contin import detect_bullish_trend_continuation, detect_bearish_trend_continuation, detect_candlestick_patterns
from patterns.mainPatterns.additional_patterns import detect_neckline_break, detect_pullback, evaluate_pattern_strength
from patterns.triangles.triangle import detect_ascending_triangle, detect_descending_triangle, detect_symmetrical_triangle
from patterns.channels.channel import detect_ascending_channel, detect_descending_channel, detect_horizontal_channel
from patterns.wedges.wedge import detect_rising_wedge, detect_falling_wedge

class SignalGenerator:
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval

    def generate_signals(self, data, generate_plot=False):
        self.data = data
        signals = []
        detected_patterns = []
        visual_data = []  # Collect data points for visualization
        plot_filename = None


        ###### DOUBLE PATTERN

        # Check for Double Top pattern
        is_double_top, top1, top2 = detect_double_top(self.data)
        if is_double_top:
            if generate_plot:
                visual_data.append(('Double Top', {'Indexes': [top1[0], top2[0]], 'Values': [top1[1], top2[1]]}))
            neckline_level = self.data['low'][top1[0]:top2[0]].min()
            neckline_break, break_index = detect_neckline_break(self.data, "double_top", neckline_level)
            if neckline_break and detect_pullback(self.data, break_index, "double_top"):
                candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "double_top")
                pattern_strength = evaluate_pattern_strength("double_top", self.data, break_index)
                detected_patterns.append(("Sell Signal after Double Top", self.data['close'][break_index], pattern_strength, candlestick_pattern))
        


        # Check for Double Bottom pattern
        is_double_bottom, bottom1, bottom2 = detect_double_bottom(self.data)
    
        # Ensure that there is a reasonable distance between the two bottoms
        if is_double_bottom and (bottom2[0] - bottom1[0] ):
            # Track the closing prices at the points of interest
            closing_prices = [self.data['close'][bottom1[0]], self.data['close'][bottom2[0]]]
            
            # Ensure the second bottom is at a similar or slightly higher level than the first bottom
            if abs(closing_prices[0] - closing_prices[1]) / closing_prices[0] < 0.05:
                
                # Identify the neckline level as the highest point between the two bottoms
                neckline_level = self.data['high'][bottom1[0]:bottom2[0]].max()
                visual_data.append(('Double Bottom', {'Indexes': [bottom1[0], bottom2[0]], 'Values': closing_prices, 'Neckline': neckline_level}))
                
                # Detect the neckline break
                neckline_break, break_index = detect_neckline_break(self.data, "double_bottom", neckline_level)
                
                # Check for pullback after the neckline break
                if neckline_break and detect_pullback(self.data, break_index, "double_bottom"):
                    candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "double_bottom")
                    pattern_strength = evaluate_pattern_strength("double_bottom", self.data, break_index)
                    detected_patterns.append(("Buy Signal after Double Bottom", self.data['close'][break_index], pattern_strength, candlestick_pattern))
                    
                    if generate_plot:
                        plot_filename = self.save_plot(visual_data, 'Double Bottom')



        ###### TRIPLE PATTERN

        # Check for Triple Top pattern
        is_triple_top, top1, top2, top3 = detect_triple_top(self.data)
        if is_triple_top:
            visual_data.append(('Triple Top', {'Indexes': [top1[0], top2[0], top3[0]], 'Values': [top1[1], top2[1], top3[1]]}))
            neckline_level = self.data['low'][top1[0]:top3[0]].min()
            neckline_break, break_index = detect_neckline_break(self.data, "triple_top", neckline_level)
            if neckline_break and detect_pullback(self.data, break_index, "triple_top"):
                candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "triple_top")
                pattern_strength = evaluate_pattern_strength("triple_top", self.data, break_index)
                detected_patterns.append(("Sell Signal after Triple Top", self.data['close'][break_index], pattern_strength, candlestick_pattern))

        # Check for Triple Bottom pattern
        is_triple_bottom, bottom1, bottom2, bottom3 = detect_triple_bottom(self.data)
        if is_triple_bottom:
            visual_data.append(('Triple Bottom', {'Indexes': [bottom1[0], bottom2[0], bottom3[0]], 'Values': [bottom1[1], bottom2[1], bottom3[1]]}))
            neckline_level = self.data['high'][bottom1[0]:bottom3[0]].max()
            neckline_break, break_index = detect_neckline_break(self.data, "triple_bottom", neckline_level)
            if neckline_break and detect_pullback(self.data, break_index, "triple_bottom"):
                candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "triple_bottom")
                pattern_strength = evaluate_pattern_strength("triple_bottom", self.data, break_index)
                detected_patterns.append(("Buy Signal after Triple Bottom", self.data['close'][break_index], pattern_strength, candlestick_pattern))

        ###### BULLISH N BEARISH TREND

        # Check for Bullish Trend Continuation pattern
        is_bullish_trend, high, low = detect_bullish_trend_continuation(self.data)
        if is_bullish_trend:
            visual_data.append(('Bullish Trend Continuation', {'Indexes': [high, low], 'Values': [self.data['high'][high], self.data['low'][low]]}))
            candlestick_pattern = detect_candlestick_patterns(self.data, high, "bullish_trend")
            pattern_strength = evaluate_pattern_strength("bullish_trend", self.data, high)
            detected_patterns.append(("Buy Signal after Bullish Trend Continuation", self.data['close'][high], pattern_strength, candlestick_pattern))

        # Check for Bearish Trend Continuation pattern
        is_bearish_trend, high, low = detect_bearish_trend_continuation(self.data)
        if is_bearish_trend:
            visual_data.append(('Bearish Trend Continuation', {'Indexes': [high, low], 'Values': [self.data['high'][high], self.data['low'][low]]}))
            candlestick_pattern = detect_candlestick_patterns(self.data, low, "bearish_trend")
            pattern_strength = evaluate_pattern_strength("bearish_trend", self.data, low)
            detected_patterns.append(("Sell Signal after Bearish Trend Continuation", self.data['close'][low], pattern_strength, candlestick_pattern))

        ###### TREND CHANGE IN BULLISH AND BEARISH MARKET

        # Check for Trend Change in Bearish Market
        is_trend_change_bearish, index = detect_trend_change_bearish(self.data)
        if is_trend_change_bearish:
            candlestick_pattern = detect_candlestick_patterns(self.data, index, "trend_change_bearish")
            pattern_strength = evaluate_pattern_strength("trend_change_bearish", self.data, index)
            detected_patterns.append(("Buy Signal after Trend Change in Bearish Market", self.data['close'][index], pattern_strength, candlestick_pattern))

        # Check for Trend Change in Bullish Market
        is_trend_change_bullish, index = detect_trend_change_bullish(self.data)
        if is_trend_change_bullish:
            candlestick_pattern = detect_candlestick_patterns(self.data, index, "trend_change_bullish")
            pattern_strength = evaluate_pattern_strength("trend_change_bullish", self.data, index)
            detected_patterns.append(("Sell Signal after Trend Change in Bullish Market", self.data['close'][index], pattern_strength, candlestick_pattern))

        ###### HEAD & SHOULDERS

        # Check for Head and Shoulders pattern
        is_head_and_shoulders, left_shoulder, head, right_shoulder = detect_head_and_shoulders(self.data)
        if is_head_and_shoulders:
            visual_data.append(('Head and Shoulders', {'Indexes': [left_shoulder[0], head[0], right_shoulder[0]], 'Values': [left_shoulder[1], head[1], right_shoulder[1]]}))
            neckline_level = min(self.data['low'][left_shoulder[0]], self.data['low'][right_shoulder[0]])
            neckline_break, break_index = detect_neckline_break(self.data, "head_and_shoulders", neckline_level)
            if neckline_break and detect_pullback(self.data, break_index, "head_and_shoulders"):
                candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "head_and_shoulders")
                pattern_strength = evaluate_pattern_strength("head_and_shoulders", self.data, break_index)
                detected_patterns.append(("Sell Signal after Head and Shoulders", self.data['close'][break_index], pattern_strength, candlestick_pattern))
            else:
                early_aggressive_entry, entry_index = detect_early_aggressive_entry(self.data, "head_and_shoulders", left_shoulder, right_shoulder)
                if early_aggressive_entry:
                    candlestick_pattern = detect_candlestick_patterns(self.data, entry_index, "head_and_shoulders")
                    pattern_strength = evaluate_pattern_strength("head_and_shoulders", self.data, entry_index)
                    detected_patterns.append(("Early Aggressive Entry Sell Signal after Head and Shoulders", self.data['close'][entry_index], pattern_strength, candlestick_pattern))

        # Check for Inverse Head and Shoulders pattern
        is_inverse_head_and_shoulders, left_shoulder, head, right_shoulder = detect_inverse_head_and_shoulders(self.data)
        if is_inverse_head_and_shoulders:
            visual_data.append(('Inverse Head and Shoulders', {'Indexes': [left_shoulder[0], head[0], right_shoulder[0]], 'Values': [left_shoulder[1], head[1], right_shoulder[1]]}))
            neckline_level = max(self.data['high'][left_shoulder[0]], self.data['high'][right_shoulder[0]])
            neckline_break, break_index = detect_neckline_break(self.data, "inverse_head_and_shoulders", neckline_level)
            if neckline_break and detect_pullback(self.data, break_index, "inverse_head_and_shoulders"):
                candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "inverse_head_and_shoulders")
                pattern_strength = evaluate_pattern_strength("inverse_head_and_shoulders", self.data, break_index)
                detected_patterns.append(("Buy Signal after Inverse Head and Shoulders", self.data['close'][break_index], pattern_strength, candlestick_pattern))
            else:
                early_aggressive_entry, entry_index = detect_early_aggressive_entry(self.data, "inverse_head_and_shoulders", left_shoulder, right_shoulder)
                if early_aggressive_entry:
                    candlestick_pattern = detect_candlestick_patterns(self.data, entry_index, "inverse_head_and_shoulders")
                    pattern_strength = evaluate_pattern_strength("inverse_head_and_shoulders", self.data, entry_index)
                    detected_patterns.append(("Early Aggressive Entry Buy Signal after Inverse Head and Shoulders", self.data['close'][entry_index], pattern_strength, candlestick_pattern))

        ###### TRIANGLES

        # Check for Ascending Triangle pattern
        is_ascending_triangle, start_index, end_index = detect_ascending_triangle(self.data)
        if is_ascending_triangle:
            visual_data.append(('Ascending Triangle', {'Indexes': [start_index, end_index], 'Values': [self.data['high'][start_index], self.data['high'][end_index]]}))
            neckline_level = self.data['high'][start_index:end_index+1].max()
            neckline_break, break_index = detect_neckline_break(self.data, "ascending_triangle", neckline_level)
            if neckline_break and detect_pullback(self.data, break_index, "ascending_triangle"):
                candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "ascending_triangle")
                pattern_strength = evaluate_pattern_strength("ascending_triangle", self.data, break_index)
                detected_patterns.append(("Buy Signal after Ascending Triangle", self.data['close'][break_index], pattern_strength, candlestick_pattern))

        # Check for Descending Triangle pattern
        is_descending_triangle, start_index, end_index = detect_descending_triangle(self.data)
        if is_descending_triangle:
            visual_data.append(('Descending Triangle', {'Indexes': [start_index, end_index], 'Values': [self.data['low'][start_index], self.data['low'][end_index]]}))
            neckline_level = self.data['low'][start_index:end_index+1].min()
            neckline_break, break_index = detect_neckline_break(self.data, "descending_triangle", neckline_level)
            if neckline_break and detect_pullback(self.data, break_index, "descending_triangle"):
                candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "descending_triangle")
                pattern_strength = evaluate_pattern_strength("descending_triangle", self.data, break_index)
                detected_patterns.append(("Sell Signal after Descending Triangle", self.data['close'][break_index], pattern_strength, candlestick_pattern))

        # Check for Symmetrical Triangle pattern
        is_symmetrical_triangle, start_index, end_index = detect_symmetrical_triangle(self.data)
        if is_symmetrical_triangle:
            visual_data.append(('Symmetrical Triangle', {'Indexes': [start_index, end_index], 'Values': [self.data['high'][start_index], self.data['low'][end_index]]}))
            neckline_level = (self.data['high'][start_index:end_index+1].max() + self.data['low'][start_index:end_index+1].min()) / 2
            neckline_break, break_index = detect_neckline_break(self.data, "symmetrical_triangle", neckline_level)
            if neckline_break and detect_pullback(self.data, break_index, "symmetrical_triangle"):
                candlestick_pattern = detect_candlestick_patterns(self.data, break_index, "symmetrical_triangle")
                pattern_strength = evaluate_pattern_strength("symmetrical_triangle", self.data, break_index)
                detected_patterns.append(("Buy Signal after Symmetrical Triangle", self.data['close'][break_index], pattern_strength, candlestick_pattern))

        ###### CHANNELS

        # Check for Ascending Channel pattern
        is_ascending_channel, start_index, end_index = detect_ascending_channel(self.data)
        if is_ascending_channel:
            visual_data.append(('Ascending Channel', {'Indexes': [start_index, end_index], 'Values': [self.data['high'][start_index], self.data['high'][end_index]]}))
            pattern_strength = evaluate_pattern_strength("ascending_channel", self.data, end_index)
            detected_patterns.append(("Buy Signal after Ascending Channel", self.data['close'][end_index], pattern_strength, False))

        # Check for Descending Channel pattern
        is_descending_channel, start_index, end_index = detect_descending_channel(self.data)
        if is_descending_channel:
            visual_data.append(('Descending Channel', {'Indexes': [start_index, end_index], 'Values': [self.data['low'][start_index], self.data['low'][end_index]]}))
            pattern_strength = evaluate_pattern_strength("descending_channel", self.data, end_index)
            detected_patterns.append(("Sell Signal after Descending Channel", self.data['close'][end_index], pattern_strength, False))

        # Check for Horizontal Channel pattern
        is_horizontal_channel, start_index, end_index = detect_horizontal_channel(self.data)
        if is_horizontal_channel:
            visual_data.append(('Horizontal Channel', {'Indexes': [start_index, end_index], 'Values': [self.data['close'][start_index], self.data['close'][end_index]]}))
            pattern_strength = evaluate_pattern_strength("horizontal_channel", self.data, end_index)
            detected_patterns.append(("Trade Signal after Horizontal Channel", self.data['close'][end_index], pattern_strength, False))

        ###### RISING AND FALLING WEDGE

        # Check for Rising Wedge pattern
        is_rising_wedge, start_index, end_index = detect_rising_wedge(self.data)
        if is_rising_wedge:
            visual_data.append(('Rising Wedge', {'Indexes': [start_index, end_index], 'Values': [self.data['high'][start_index], self.data['high'][end_index]]}))
            pattern_strength = evaluate_pattern_strength("rising_wedge", self.data, end_index)
            detected_patterns.append(("Sell Signal after Rising Wedge", self.data['close'][end_index], pattern_strength, False))

        # Check for Falling Wedge pattern
        is_falling_wedge, start_index, end_index = detect_falling_wedge(self.data)
        if is_falling_wedge:
            visual_data.append(('Falling Wedge', {'Indexes': [start_index, end_index], 'Values': [self.data['low'][start_index], self.data['low'][end_index]]}))
            pattern_strength = evaluate_pattern_strength("falling_wedge", self.data, end_index)
            detected_patterns.append(("Buy Signal after Falling Wedge", self.data['close'][end_index], pattern_strength, False))

        # Select the best pattern based on pattern strength
        if detected_patterns:
            best_pattern = max(detected_patterns, key=lambda x: x[2])
            pattern_message = f" (Candlestick Pattern: {best_pattern[3]})" if best_pattern[3] else ""
            signals.append(f"{best_pattern[0]} Price at {best_pattern[1]}{pattern_message}")

            # Save the plot if required
            if generate_plot:
                plot_filename = self.save_plot(visual_data, best_pattern[0])

        return signals if signals else ["No Signal"], plot_filename

    def save_plot(self, visual_data, pattern_name):
        # Extract the OHLC data
        ohlc_data = self.data[['open', 'high', 'low', 'close']]

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot the candlestick chart
        mpf.plot(ohlc_data, type='candle', ax=ax, style='charles', show_nontrading=True)

        # Overlay the pattern points on the candlestick chart
        for pattern in visual_data:
            if pattern[0] == pattern_name:
                # Plot the bottoms with annotations
                for i, (index, value) in enumerate(zip(pattern[1]['Indexes'], pattern[1]['Values'])):
                    ax.scatter(self.data.index[index], value, color='red', s=100, zorder=5)
                    ax.annotate(f'Bottom {i+1}\n{value:.2f}', (self.data.index[index], value),
                                textcoords="offset points", xytext=(0,10), ha='center', fontsize=10,
                                bbox=dict(boxstyle="round,pad=0.3", edgecolor="red", facecolor="white"))
                
                # Draw a line connecting the bottoms
                bottom_indexes = pattern[1]['Indexes']
                ax.plot([self.data.index[bottom_indexes[0]], self.data.index[bottom_indexes[1]]],
                        [pattern[1]['Values'][0], pattern[1]['Values'][1]], color='green', linestyle='--', linewidth=2)

                # Draw the neckline
                neckline_level = pattern[1]['Neckline']
                ax.axhline(neckline_level, color='blue', linestyle='--', linewidth=1.5, label=f'Neckline: {neckline_level:.2f}')
                ax.annotate(f'Neckline\n{neckline_level:.2f}', xy=(self.data.index[pattern[1]['Indexes'][1]], neckline_level),
                            xytext=(self.data.index[pattern[1]['Indexes'][1]], neckline_level + 0.05 * neckline_level),
                            arrowprops=dict(facecolor='blue', shrink=0.05), fontsize=10, color='blue')

        # Ensure the legend is visible
        ax.legend(loc='best')

        # Set the title and labels
        ax.set_title(f'{self.symbol} - {pattern_name}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        ax.grid(True)

        # Save the plot to a file
        plot_filename = f'{pattern_name}_plot.png'
        plt.savefig(plot_filename)
        plt.close()

        return plot_filename
