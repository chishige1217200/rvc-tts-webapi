from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import app as tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ReactアプリのURL
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/generate/")
async def generate(text: str):
    try:
        data = await tts.generate_audio(text)
        return StreamingResponse(data, media_type="audio/wav", headers={"Content-Disposition": "inline; filename=data.wav"})
    except Exception as e:
        return {"error": f"{e}"}

# サーバー上の音声ファイルのパス
EDGE_AUDIO_FILE_PATH = "edge_output.mp3"
TTS_AUDIO_FILE_PATH = "tts_output.wav"


def iterfile(filePath):
    # ファイルをバイナリモードで開き、ストリームとして返す
    try:
        with open(filePath, "rb") as file:
            yield from file
    except:
        raise


@app.get("/download-edge/")
async def download_edge():
    try:
        if os.path.isfile(TTS_AUDIO_FILE_PATH) == False:
            raise FileNotFoundError("ファイルが存在しません")

        # ファイルを直接返す
        return FileResponse(
            path=EDGE_AUDIO_FILE_PATH,
            media_type="audio/mpeg",
            filename=EDGE_AUDIO_FILE_PATH  # クライアント側でのダウンロード名
        )
    except Exception as e:
        return {"error": f"{e}"}


@app.get("/play-edge/")
async def play_edge():
    try:
        if os.path.isfile(EDGE_AUDIO_FILE_PATH) == False:
            raise FileNotFoundError("ファイルが存在しません")

        # ファイルをストリーミングする
        return StreamingResponse(iterfile(EDGE_AUDIO_FILE_PATH), media_type="audio/mpeg")
    except Exception as e:
        return {"error": f"{e}"}


@app.get("/download-tts/")
async def download_tts():
    try:
        if os.path.isfile(TTS_AUDIO_FILE_PATH) == False:
            raise FileNotFoundError("ファイルが存在しません")

        # ファイルを直接返す
        return FileResponse(
            path=TTS_AUDIO_FILE_PATH,
            media_type="audio/wav",
            filename=TTS_AUDIO_FILE_PATH  # クライアント側でのダウンロード名
        )
    except Exception as e:
        return {"error": f"{e}"}


@app.get("/play-tts/")
async def play_tts():
    try:
        if os.path.isfile(TTS_AUDIO_FILE_PATH) == False:
            raise FileNotFoundError("ファイルが存在しません")
        # ファイルをストリーミングする
        return StreamingResponse(iterfile(TTS_AUDIO_FILE_PATH), media_type="audio/wav")
    except Exception as e:
        return {"error": f"{e}"}
