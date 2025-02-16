import argparse
import asyncio
import json
import os
import ssl
import traceback
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer

ROOT = os.path.dirname(__file__)
pcs = set()

async def index(request):
    try:
        with open(os.path.join(ROOT, "index.html"), "r") as f:
            content = f.read()
        return web.Response(content_type="text/html", text=content)
    except Exception as e:
        tb = traceback.format_exc()
        print("Error reading index.html:", tb)
        return web.Response(
            status=500,
            content_type="application/json",
            text=json.dumps({"error": str(e), "traceback": tb}),
        )

async def offer(request):
    try:
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        pc = RTCPeerConnection()
        pcs.add(pc)
        print("Created PeerConnection for", request.remote)

        # Open the local video device with options to reduce verbose output.
        try:
            player = MediaPlayer(
                "/dev/video0",
                format="v4l2",
                options={
                    "loglevel": "error",       # Suppress FFmpeg logs
                    "video_size": "640x480",     # Fixed resolution
                    "framerate": "30"            # Fixed framerate
                }
            )
        except Exception as e:
            tb = traceback.format_exc()
            print("Error opening MediaPlayer:", tb)
            return web.Response(
                status=500,
                content_type="application/json",
                text=json.dumps(
                    {"error": "Could not open video device: " + str(e), "traceback": tb}
                ),
            )

        # Add media tracks from the server’s video (and audio, if available).
        if player.video:
            pc.addTrack(player.video)
        if player.audio:
            pc.addTrack(player.audio)

        @pc.on("iceconnectionstatechange")
        def on_ice_state_change():
            print("ICE connection state is", pc.iceConnectionState)
            if pc.iceConnectionState == "failed":
                asyncio.ensure_future(pc.close())

        @pc.on("connectionstatechange")
        def on_connectionstatechange():
            print("Connection state is", pc.connectionState)
            if pc.connectionState == "closed":
                try:
                    player.stop()
                except Exception as e:
                    print("Error stopping player:", e)

        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)
        print("Sending answer to", request.remote)

        response = {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
        return web.json_response(response)
    except Exception as e:
        tb = traceback.format_exc()
        print("Error in /offer:", tb)
        return web.Response(
            status=500,
            content_type="application/json",
            text=json.dumps({"error": str(e), "traceback": tb}),
        )

async def on_shutdown(app):
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebRTC Video Call Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to listen on")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("--cert-file", help="SSL certificate file (optional)")
    parser.add_argument("--key-file", help="SSL key file (optional)")
    args = parser.parse_args()

    ssl_context = None
    if args.cert_file and args.key_file:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(args.cert_file, args.key_file)

    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_post("/offer", offer)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host=args.host, port=args.port, ssl_context=ssl_context)
