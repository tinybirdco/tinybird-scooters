# Scooter IoT Analytics Demo

This demo uses streaming IoT time series data from Confluent Cloud on AWS plus scooter dimensional tables in Amazon S3 to create real-time Scooter IoT Analytics for visualization in a frontend application (we used Retool).

## Instructions

### 1. Set up a free Tinybird Workspace

Navigate to [tinybird.co/signup](https://www.tinybird.co/signup) and create a free account. Create a new Workspace (name it whatever you want).

### 2. Clone the repository

```bash
git clone https://github.com/tinybirdco/tinybird-scooters.git
cd tinybird-scooters
```

### 3. Install the Tinybird CLI and dependencies

```bash
python -mvenv .e
. .e/bin/activate
pip install tinybird-cli ndjson confluent_kafka
```

### 4. Authenticate to Tinybird

Copy your user admin token from [ui.tinybird.co/tokens](https://ui.tinybird.co/tokens). Your user admin token is the token with the format `admin <your email address>`.

In the Tinybird CLI, run the following command

```bash
cd tinybird
export TB_TOKEN=<your user admin token>
tb auth -i
```

If you intend to push this to your own repo, add the `.tinyb` file to your `.gitignore`, as it contains your user admin token.

```bash
echo ".tinyb" >> .gitignore
```

### Update `data_gen.py` with your Confluent cluster details

This demo uses Confluent Cloud to handle data streaming of scooter telemetry events. If you're new to Confluent, you can signup for an account [here](https://www.confluent.io/get-started). We use a Python script to generate fake data and send it to Confluent Cloud. You'll need to update the `data_gen.py` file with your Confluent details:

```python
CONFLUENT_SERVER = 'your_confluent_bootstrap_server'
CONFLUENT_KEY = 'your_confuent_access_key'
CONFLUENT_SECRET = 'your_confluent_access_secret'
```

Once you've done that, run the data generator to begin sending data to your Confluent topic:

```bash
python data_gen.py
```

### Create a the scooter telemetry events Data Source in Tinybird

You're going to capture streaming data from Confluent into Tinybird so you can query it and build your APIs.

You can do this in the Tinybird UI using the [Confluent Connector](https://www.tinybird.co/docs/ingest/confluent.html), or in the CLI using the following command:

```bash
tb connection create kafka
# Kafka Bootstrap Server: <your Confluent server>
# Key: <your Confluent access key>
# Secret: <your Confluent secret>
# Connection name: <Give your connection a name, defaults to bootstrap server>
```

Then, update the `scooter_telem_events.datasource` file as follows:

```
SCHEMA >
    `battery_percent` Int16 `json:$.battery_percent`,
    `fault_severity` String `json:$.fault_severity`,
    `journey_id` String `json:$.journey_id`,
    `latitude` Float32 `json:$.latitude`,
    `longitude` Float32 `json:$.longitude`,
    `scooter_id` String `json:$.scooter_id`,
    `status` String `json:$.status`,
    `timestamp` DateTime `json:$.timestamp`

ENGINE "MergeTree"
ENGINE_PARTITION_KEY "toYear(timestamp)"
ENGINE_SORTING_KEY "timestamp"

KAFKA_CONNECTION_NAME <your connection name>
KAFKA_TOPIC <your Confluent topic>
KAFKA_GROUP_ID <choose a consumer group ID>
```

### Create a scooter info Data Source

You're going to enrich scooter telemetry events with dimensions in S3. To do that, upload the [`scooter_info.csv`](/tinybird/scripts/scooter_info.csv) to an S3 bucket, and use the [S3 Connector](https://www.tinybird.co/docs/ingest/s3.html) to sync that file to Tinybird.

Alternatively, you can simply upload the `scooter_info.csv` file to Tinybird directly.

### Push the remaining resources to the Tinybird server

Push the remaining Pipes and Data Sources to Tinybird with...

```
tb push
```

### Build a frontend!

You'll now have several Tinybird APIs that you can build with. We used Retool to build a simple frontend application. If you'd like to see how we did that, watch the [recording of our live coding session](https://www.youtube.com/watch?v=rf7ZannHDf0)

## Contributing

If you find any issues or have suggestions for improvements, please submit an issue or a [pull request](https://github.com/tinybirdco/scooter-rental-iot-analytics/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc).

## License

This code is available under the MIT license. See the [LICENSE](https://github.com/tinybirdco/scooter-rental-iot-analytics/blob/main/LICENSE.txt) file for more details.

## Need help?

&bull; [Community Slack](https://www.tinybird.co/community) &bull; [Tinybird Docs](https://www.tinybird.co/docs) &bull;

## Authors

- [Cameron Archer](https://github.com/tb-peregrine)
- [Alasdair Brown](https://github.com/sdairs)
