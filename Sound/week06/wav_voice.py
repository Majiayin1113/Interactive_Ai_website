import os
import sys
import subprocess
import torch
import torchaudio as ta

# Try to import chatterbox; if not available we'll fall back to pyttsx3
HAVE_CHATTERBOX = True
try:
	from chatterbox.tts import ChatterboxTTS
	from chatterbox.mtl_tts import ChatterboxMultilingualTTS
except Exception:
	HAVE_CHATTERBOX = False

# Base output directory (updated to the requested path)
BASE_DIR = r'F:\PolyU\Sem1\5913Programming'
os.makedirs(BASE_DIR, exist_ok=True)


def _install_package(package_name: str):
	"""Install a pip package into the current Python environment."""
	print(f"Installing {package_name}...")
	subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


if HAVE_CHATTERBOX:
	device = "cuda" if torch.cuda.is_available() else "cpu"
	model = ChatterboxTTS.from_pretrained(device=device)

	text = (
		"Ezreal and Jinx teamed up with Ahri, Yasuo, and Teemo to take down the enemy's Nexus "
		"in an epic late-game pentakill."
	)
	wav = model.generate(text)
	ta.save(os.path.join(BASE_DIR, "test-english.wav"), wav, model.sr)

	# Multilingual examples
	multilingual_model = ChatterboxMultilingualTTS.from_pretrained(device=device)

	chinese_text = "你好，今天天气真不错，希望你有一个愉快的周末。"
	wav_chinese = multilingual_model.generate(chinese_text, language_id="zh")
	ta.save(os.path.join(BASE_DIR, "test-chinese.wav"), wav_chinese, model.sr)

	print("Generated WAV files using Chatterbox and saved to:")
	print(os.path.join(BASE_DIR, "test-english.wav"))
	print(os.path.join(BASE_DIR, "test-chinese.wav"))
else:
	# Fallback: use pyttsx3 to synthesize WAV files (offline, cross-platform)
	try:
		import pyttsx3
	except Exception:
		# Attempt to install pyttsx3 then import again
		_install_package("pyttsx3")
		import pyttsx3

	engine = pyttsx3.init()

	# English fallback
	english_text = (
		"Ezreal and Jinx teamed up with Ahri, Yasuo, and Teemo to take down the enemy's Nexus "
		"in an epic late-game pentakill."
	)
	out_path_en = os.path.join(BASE_DIR, "test-english.wav")
	print(f"Synthesizing English fallback to {out_path_en}")
	engine.save_to_file(english_text, out_path_en)
	engine.runAndWait()

	# Chinese fallback (pyttsx3 may not have a Chinese-capable voice; it will still create the file)
	chinese_text = "你好，今天天气真不错，希望你有一个愉快的周末。"
	out_path_zh = os.path.join(BASE_DIR, "test-chinese.wav")
	print(f"Synthesizing Chinese fallback to {out_path_zh}")
	engine.save_to_file(chinese_text, out_path_zh)
	engine.runAndWait()

	print("Fallback synthesis complete. Saved WAVs to:")
	print(out_path_en)
	print(out_path_zh)

# If you'd like to use a different TTS backend (gTTS, edge-tts, etc.) modify this file.