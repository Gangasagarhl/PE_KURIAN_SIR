import asyncio
import json
import logging
import cv2

import aiohttp
from aiortc import RTCPeerConnection, RTCSessionDescription

async def run_offer():
    pc = RTCPeerConnection()

    # Instead of capturing local media, we signal that we want to receive video/audio.
    const_options = {
        "offerToReceiveVideo": True,
        "offerToReceiveAudio": True
    }
    offer = await pc.createOffer(const_options)
    await pc.setLocalDescription(offer)

    # When a remote track is received, display it.
    @pc.on("track")
    def on_track(track):
        print("Client received", track.kind, "track")
        if track.kind == "video":
            asyncio.ensure_future(run_video_display(track))

    # Send the offer to the server.
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8080/offer", json={
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        }) as resp:
            if resp.status != 200:
                text = await resp.text()
                print("Error response from server:", text)
                return
            response_json = await resp.json()

    if "sdp" not in response_json:
        print("Unexpected response from server:", response_json)
        return

    answer = RTCSessionDescription(sdp=response_json["sdp"], type=response_json["type"])
    await pc.setRemoteDescription(answer)
    print("Connection established. Press Ctrl+C to exit.")
    await asyncio.sleep(3600)

async def run_video_display(track):
    while True:
        try:
            frame = await track.recv()
            img = frame.to_ndarray(format="bgr24")
            cv2.imshow("Client Received", img)
            cv2.waitKey(1)
        except Exception as e:
            print("Video display ended:", e)
            break

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_offer())
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
