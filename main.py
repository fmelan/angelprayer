import datetime

from auth_api import get_access_token
from position_api import PositionData, GeographicPosition, send_position_report, Target, Identifier, Height, \
    GeographicVector, PositionReport


def get_test_tokens():
    data = {
        'client_id': 'RziveGzb0G4z6M-1cFQkE6MRhTVtWX2U8pna0klD0',
        'client_secret': 'RziveGzb0G4z6M-1cFQkE6MRhTVtWX2U8pna0klD0',
        'redirect_uri': "localhost",
        'device_id': "DroneTag"
    }

    return get_access_token(**data)


if __name__ == '__main__':
    # The access and refresh tokens should ideally be stored on the client to prevent the user having to authenticate
    # repeatedly. How to store these is beyond the scope of this tutorial, but a client-side cookie, local storage
    # etc could be used.

    # try:
    #     tokens = get_test_tokens()
    # except AngelError as e:
    #     print(e.status_code)
    #     print(e.json())
    #
    # print(tokens.dict())
    # print(tokens.access_token)


    # debugging and trying to send position report data

    access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjVkMTg1MTAyIiwieDV0IjoiSndBMXF5OHlPbGNfZERLZ1BGUm02S3VlSXE4IiwidHlwIjoiSldUIiwidmVyIjoxfQ.eyJ1bmlxdWVfbmFtZSI6IkRyb25lVGFnIiwidXJuOmFhOnRva2VuX3R5cGUiOiJkZXZpY2UiLCJ1cm46YWE6ZGV2aWNlX2lkIjoidXJuOmFhOmRldmljZTpSeml2ZUd6YjBHNHo2TS0xY0ZRa0U2TVJoVFZ0V1gyVThwbmEwa2xEMDpEcm9uZVRhZyIsInVybjphYTp0ZW5hbnRfaWQiOiJkZWZhdWx0IiwidXJuOm9hdXRoOnNjb3BlIjoic3VydmVpbGxhbmNlX2FwaSIsIm5iZiI6MTY0ODczODg0MywiZXhwIjoxNjQ4ODI1MjQzLCJpYXQiOjE2NDg3Mzg4NDMsImlzcyI6IkFBLkF1dGgiLCJhdWQiOiJBQSBTZXJ2aWNlcyJ9.ATDLpH1iRS6SfB_7bz2ZY2EndPmRfCd_jPrYmOD9cwpMn7YL9CXGuOs7OICLvfY_qsJQPx9OXMgzo4YBSubb2pOO54Xb0nhHH8I9juxRIhVLIy6zuAEoaBmrIplJYX11kSXTdlaiQBhpg2PyttshL8LXtbd9maeEj3C4NQt5tOMvM2b7dFThsXHBe-OBNb84lh5ML_t9kpHS1DlUNTNlh9EAgLjSwLm88KxZHzssgTFrRPZqH67LV3Cri5xNh-Vj3XuiRAWrkfKf9OzVArs1Ukot1LoevVy0berr8JEBxxTJkAznMytqTmMZrowzXFr_FHKh8WZMXT3b5aqK5REEMg"

    position = GeographicPosition(lat=52.07096461036907, lon=-0.6322133544584766)
    target_ids = [Identifier(id="123456",type="SerialNumber")]
    target = Target(ids=target_ids)
    altitudes = [Height(height=123, datum="msl")]
    groundVelocity = GeographicVector(x=0,y=0,z=0)
    pos_data = PositionData(id='1', sourceTimeStamp=datetime.datetime.now(),
                            position=position, target=target, altitudes=altitudes,
                            groundVelocity=groundVelocity)
    pos_report = PositionReport(positions=[pos_data])

    print("Sending position data...")

    position_report_data = pos_report.json(exclude_unset=True)
    print(position_report_data)

    response = send_position_report(access_token, position_report_data)

    print(f"response: {response.status_code}")

    assert response.status_code == 202
