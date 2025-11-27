import speedtest


def run_ookla_speedtest():
    st = speedtest.Speedtest()

    st.get_servers()
    st.get_best_server()

    # Run tests
    download = st.download()
    upload = st.upload()
    ping = st.results.ping

    # Get full result dict
    results = st.results.dict()

    return results
