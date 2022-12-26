# Option Trading Alerts (OTAs)

<!-- ABOUT THE PROJECT -->
## About The Project
This system is intended to be read Discord servers (e.g. GOAT Options or OBR Investing) channel alerts. 
The system is capable of scanning given channels (e.g Channel IDs) for newest messages matching stock or option
trading alerts. These alerts should include asset ticker, expire date, premium, and strike price. Eventually, the system will be able to create and close trades from the alerts scanned using limit orders (e.g. stop loss and trailing stop limit orders).

## Getting Started

### Installation
```bash
git clone git@github.com:option_trading_alerts
dpkg -i option_trading_alerts
```

#### A. Running Locally
```bash
python -m option_trading_alerts

start scanning-discord --testing True
```

#### B. Running on Cloud

## Contributing
Pull requests are always welcome. 
For major changes, please open an issue first describing your proposed changes.
 
Please ensure all tests are passing with pull requests to help expedite review time lines.

## License

[MIT](https://choosealicense.com/licenses/mit/)
