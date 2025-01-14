
# BitFinex Investment Prognosis

A Python tool that interacts with the Bitfinex API to analyze your cryptocurrency investments, providing insights and calculating the required price to reach a specified target value in USD.

This project is designed to be beginner-friendly, with extensive in-line comments to explain the functionality of the code. It aims to serve as both a useful tool for cryptocurrency enthusiasts and a learning resource for those new to Python programming.

## Features

- Calculates total USD investment in BTC. (The actual Dollar amount used to purchase BTC)
- Calculates the total USD investment with the current BTC price. (The value of that investment, as it is with the current BTC price)
- Fetches BTC balance and transaction history from Bitfinex.
- Retrieves the current BTC/USD price.
- Calculates the required BTC price to achieve a target USD value.
- Provides a detailed breakdown in a tabular format.

## Planned Updates

This is the first version of the tool. In upcoming updates, the following features are planned:

1. **Object Orientation**: Transition from a procedural approach to object-oriented programming.
2. **Multiple Currencies**: Support for other fiat currencies besides USD.
3. **Additional Cryptocurrencies**: Include support for other cryptocurrencies like ETH.
4. **Investment Breakdown**: Analyze your investments by cryptocurrency and display their current value.
5. **Performance Statistics**: Show which investments performed the best within a user-selected timeframe.

### Scope of the Project

This tool is designed exclusively for the BitFinex API and will not support other cryptocurrency exchange platforms. The focus is on providing insights for BitFinex users without requiring accounts on additional exchanges.

## Requirements

To make this as user-friendly as possible, here are instructions for installing Python 3.6 or higher on your operating system:

- [Windows](https://www.python.org/downloads/windows/)
- [macOS](https://www.python.org/downloads/macos/)
- [Linux](https://docs.python-guide.org/starting/install3/linux/)

This script requires two additional Python libraries (called "dependencies" because the script depends on them):
- **`requests`**: Used for making HTTP requests to the Bitfinex API.
- **`prettytable`**: Used to display data in a table format.

To install these libraries, run the following command in your terminal or command prompt:
```bash
pip install requests prettytable
```

> **Note**: Depending on your setup, you might need to use `pip3` instead of `pip`. 
> 
> If you need to use `pip3` instead of `pip`, you will likely also need to use `python3` instead of `python` to execute the script in the following steps. 
> 
> Additionally, ensure `pip` is installed, as it may not be included with some Python installations. Refer to the official Python documentation for guidance.

## Usage

### Setting Up Your API Key

1. Log in to your Bitfinex account.
2. Navigate to the **API Key Management** section by selecting the silhouette icon in the top-right corner of the screen. Alternatively, use this direct [link to the API Key management page](https://setting.bitfinex.com/api) or [this link to create a new key directly](https://setting.bitfinex.com/api#new-key).
3. Create a new API Key and select the following permissions:
   - **Get historical balances entries and trade information**
   - **Get wallet balances and addresses**
   - **Optional**: Allow access from any IP if you don't wish to restrict access to specific IP addresses.

> **Important**: For safety, all other permissions should be turned off unless explicitly required. This ensures the API Key has read-only access, preventing it from performing transactions or modifying your account.

4. Copy the API Key and Secret and paste them into the script, replacing the placeholder text:
   ```python
   API_KEY = "your_API_key"
   API_SECRET = "your_API_secret"
   ```

### Running the Script

1. **Download the script**: If you are familiar with Git, clone the repository. If not, simply download the `.py` file from this repository.
   - To clone the repository using Git, follow [this guide](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository). If you are new to GitHub and want to learn more about version control systems, start [here](https://docs.github.com/en/get-started).
   - Alternatively, you can download or copy/paste the source code directly.

2. Open a terminal or command prompt, navigate to the folder containing the script, and run it:
   ```bash
   python crypto_prognosis.py
   ```

3. Use command-line arguments for additional functionality:
   - Specify a target value using `--target`. Examples:
     ```bash
     python crypto_prognosis.py --target 200
     python crypto_prognosis.py --target 30.50
     ```
   - Adjust debug output using `--debug-level`. Example:
     ```bash
     python crypto_prognosis.py --debug-level 2
     ```
     Debug levels:
     - `0`: No debug output (default).
     - `1`: Debug output to the console.
     - `2`: Debug output to both the console and a log file (`debug_log.txt`).
     - `3`: Debug output to the log file only.

## Output

The script generates two tables:
1. **Overview**: Shows BTC balance, current USD value, and total investment.
2. **Analysis**: Displays the target value (USD), current BTC price, required price, price difference, and percentage change.

### Example

```text
+-------------------------+----------------+
|       Description       |      Value     |
+-------------------------+----------------+
|       BTC Balance       | 0.00086264 BTC |
|   Current Value (USD)   |    79.48 $     |
| Total Investment (USD)  |    80.36 $     |
+-------------------------+----------------+

+--------------------------+------------------------+
|       Description        |          Value         |
+--------------------------+------------------------+
|      Target Value (USD)  |         200.00 $       |
|     Current BTC Price    |       92,000.00 $      |
|    Required BTC Price    |      231,846.42 $      |
|      Price Difference    |      139,846.42 $      |
|     Percentage Change    |        151.90 %        |
+--------------------------+------------------------+
```

## License

This project is licensed under the [MIT License](LICENSE).

## Note on License Changes

Currently, this project uses the MIT License, allowing unrestricted use, modification, and distribution. However, the license may change in future updates to require attribution for its use. Always check the repository for the latest licensing terms.
