============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: C:\source\IAResipa
plugins: anyio-4.9.0, langsmith-0.4.6, cov-6.2.1, json-report-1.5.0, metadata-3.1.1, mock-3.14.1
collected 14 items

tests\unit\test_py_04_reservation_manager.py ...........                 [ 78%]
tests\08.responderaoUsuario\test_response_generator.py ...               [100%]

============================== warnings summary ===============================
tests/unit/test_py_04_reservation_manager.py::test_check_active_reservations_found
  C:\Program Files\Python313\Lib\site-packages\supabase\_sync\client.py:303: DeprecationWarning: The 'timeout' parameter is deprecated. Please configure it in the http client instead.
    return SyncPostgrestClient(

tests/unit/test_py_04_reservation_manager.py::test_check_active_reservations_found
  C:\Program Files\Python313\Lib\site-packages\supabase\_sync\client.py:303: DeprecationWarning: The 'verify' parameter is deprecated. Please configure it in the http client instead.
    return SyncPostgrestClient(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================= 14 passed, 2 warnings in 5.27s ========================
