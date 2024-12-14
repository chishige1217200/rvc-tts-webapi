from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import app as tts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ReactアプリのURL
    allow_methods=["*"],
    allow_headers=["*"],
)

# サーバー上の音声ファイルのパス
AUDIO_FILE_PATH = "edge_output.mp3"


@app.get("/generate-audio/")
async def generate_audio(text: str):
    try:
        data = await tts.generate_audio(text)
        return StreamingResponse(data, media_type="audio/wav", headers={"Content-Disposition": "inline; filename=data.wav"})
    except:
        return {"Error": "音声合成に失敗しました。"}

@app.get("/download-audio/")
async def download_audio():
    try:
        # ファイルを直接返す
        return FileResponse(
            path=AUDIO_FILE_PATH,
            media_type="audio/mpeg",
            filename="edge_output.mp3"  # クライアント側でのダウンロード名
        )
    except FileNotFoundError:
        return {"error": "File not found"}

@app.get("/play-audio/")
async def generate_audio():
    # ファイルをバイナリモードで開き、ストリームとして返す
    def iterfile():
        with open(AUDIO_FILE_PATH, "rb") as file:
            yield from file

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
