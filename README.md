# Scooter IoT Analytics Demo

This demo uses streaming IoT time series data from Confluent Cloud on AWS plus scooter dimensional tables in Amazon S3 to create real-time Scooter IoT Analytics for visualization in a frontend application (we've used Retool).

## Instructions

### 1. Set up a free Tinybird Workspace

Navigate to [tinybird.co/signup](https://www.tinybird.co/signup) and create a free account. Create a new Workspace (name it whatever you want).

### 2. Clone the repository

```bash
git clone https://github.com/tinybirdco/scooter-rental-iot-analytics.git
cd scooter-rental-iot-analytics
```

### 3. Install the Tinybird CLI

```bash
python -mvenv .e
. .e/bin/activate
pip install tinybird-cli
```

### 4. Authenticate to Tinybird

Copy your user admin token from [ui.tinybird.co/tokens](https://ui.tinybird.co/tokens). Your user admin token is the token with the format `admin <your email address>`.

In the Tinybird CLI, run the following command

```bash
cd data-project
export TB_TOKEN=<your user admin token>
tb auth
```

If you intend to push this to your own repo, add the `.tinyb` file to your `.gitignore`, as it contains your user admin token.

```bash
echo ".tinyb" >> .gitignore
```

### TBD

---

## Contributing

If you find any issues or have suggestions for improvements, please submit an issue or a [pull request](https://github.com/tinybirdco/scooter-rental-iot-analytics/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc).

## License

This code is available under the MIT license. See the [LICENSE](https://github.com/tinybirdco/scooter-rental-iot-analytics/blob/main/LICENSE.txt) file for more details.

## Need help?

&bull; [Community Slack](https://www.tinybird.co/community) &bull; [Tinybird Docs](https://www.tinybird.co/docs) &bull;

## Authors

- [Cameron Archer](https://github.com/tb-peregrine)
- [Alasdair Brown](https://github.com/sdairs)
