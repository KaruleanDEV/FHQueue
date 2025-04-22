logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load environment variables
CurrentPlayer = os.environ.get('CURRENT_PLAYER_URL', 'PLACEHOLDER')
ShardStatus = os.environ.get('SHARD_STATUS_URL', 'PLACEHOLDER')

# dictionary
gauge_dict = {}
start_http_server(8500)

# main
while True:
    try:
        # Get ShardStatus data
        session = Session()
        r = session.get(ShardStatus)
        r.raise_for_status()
        data = r.json()
        #logging
        logging.info(f"{time.strftime('%H:%M:%S')} SteamShards: {r.status_code} {r.reason}")
        GlobalPopulation.set(data['normalizedGlobalPopulation'])
        
        # Update
        for i in data['serverConnectionInfoList']:
            if all(key in i for key in ['currentMap', 'wardenQueueSize', 'colonialQueueSize']):
                current_map = i['currentMap']
                warden_queue_size = i['wardenQueueSize']
                colonial_queue_size = i['colonialQueueSize']
        
                gauge_key = f'{current_map}_WardenQueue'
                if gauge_key in gauge_dict:
                    gauge_dict[gauge_key].set(warden_queue_size)
                else:
                    gauge_dict[gauge_key] = Gauge(gauge_key, f'{current_map} Queue Warden')
                    gauge_dict[gauge_key].set(warden_queue_size)

        # Get CurrentPlayer data
        q = session.get(CurrentPlayer)
        # Logging
        logging.info(f"{time.strftime('%H:%M:%S')} SteamShards: {r.status_code} {r.reason}")
        q.raise_for_status()
        qdata = q.json()
        CurrentlyPlaying.set(qdata['response']['player_count'])

        time.sleep(60)
    except requests.exceptions.RequestException as e:
        print('Exception occurred:', str(e))
