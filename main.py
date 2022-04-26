import datetime

from fastapi import FastAPI

from position_api import PositionData, GeographicPosition, send_position_report, Target, Identifier, Height, \
    GeographicVector, PositionReport
from settings import settings

app = FastAPI()


@app.get("/")
def read_root():
    return "Let's pray to Altitude Angel."


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
    # print(tokens.refresh_token)

    # debugging and trying to send position report data

    # access_token = settings.access_token
    #
    # position = GeographicPosition(lat=52.07096461036907, lon=-0.6322133544584766)
    # target_ids = [Identifier(id="123456", type="SerialNumber")]
    # target = Target(ids=target_ids)
    # altitudes = [Height(height=123, datum="msl")]
    # groundVelocity = GeographicVector(x=0, y=0, z=0)
    # pos_data = PositionData(id='1', sourceTimeStamp=datetime.datetime.now(),
    #                         position=position, target=target, altitudes=altitudes,
    #                         groundVelocity=groundVelocity)
    # pos_report = PositionReport(positions=[pos_data])
    #
    # print("Sending position report ...")
    #
    # print(pos_report.json(exclude_unset=True))
    #
    # response = send_position_report(access_token, pos_report)
    #
    # print(f"response: {response.status_code}")
    #
    # # check success
    # assert response.status_code == 202

    print(settings.access_token)