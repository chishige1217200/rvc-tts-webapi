import os
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ReactアプリのURL
    allow_methods=["*"],
    allow_headers=["*"],
)

# サーバー上の音声ファイルのパス
AUDIO_FILE_PATH = "tts_output.wav"

@app.get("/")
async def generate_audio():
    try:
        # ファイルをバイナリモードで開き、ストリームとして返す
        def iterfile():
            with open(AUDIO_FILE_PATH, "rb") as file:
                yield from file

        return StreamingResponse(iterfile(), media_type="audio/wav")
    except FileNotFoundError:
        return {"error": "File not found"}

# @app.get("/download-audio/")
# async def download_audio():
#     try:
#         # ファイルを直接返す
#         return FileResponse(
#             path=AUDIO_FILE_PATH,
#             media_type="audio/mpeg",
#             filename="audio_file.mp3"  # クライアント側でのダウンロード名
#         )
#     except FileNotFoundError:
#         return {"error": "File not found"}

# @app.get("/generate-audio/")
# async def generate_audio():
#     # ダミーのMP3データ（本番では適切な音声生成や読み込みを行う）
#     audio_content = BytesIO(b"Dummy MP3 data")
#     return StreamingResponse(
#         content=audio_content,
#         media_type="audio/mpeg",
#         headers={"Content-Disposition": "inline; filename=generated_audio.mp3"}
#     )