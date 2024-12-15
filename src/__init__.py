
def debug():
    import debugpy
    debugpy.listen(('127.0.0.1', 5678))
    print("Waiting for debugger attach")
    debugpy.wait_for_client()
    print("Debugger attached")
    from webapps_manager import application
    application.main()