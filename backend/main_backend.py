from audio_extractor import extract_audio
from transcriber import transcribe_audio
from retriever import build_retriever
from qa_chain import build_qa_chain, query_video, generate_summary

import asyncio

async def main():
	# video_path = "backend/input_video.mp4"
	# audio_path = extract_audio(video_path)
	# transcript_path = await transcribe_audio(audio_path, model_size="base", translate_to="zh-cn")
	retriever = build_retriever("processed_transcript_timestamped.txt")
	chain = build_qa_chain(retriever)
	summary = generate_summary(chain, retriever)
	print("摘要:", summary)
	response = query_video(chain, "视频主要讲什么？", [])
	print("回答:", response)

asyncio.run(main())