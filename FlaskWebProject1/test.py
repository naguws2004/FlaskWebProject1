from transformers import pipeline
import scipy

# Create the pipeline
music_gen = pipeline("text-to-audio", "facebook/musicgen-large")

# Define prompt for audio generation
prompt = """Generate a smooth jazz piece reminiscent of classic elevator music. The track should feature soft saxophone melodies, gentle piano chords, and a relaxed double bass line, creating a calm and sophisticated ambiance. The tempo should be slow to medium, with a soothing and mellow vibe throughout."""

# Generate music
music = music_gen(prompt, forward_params={"do_sample": True})

scipy.io.wavfile.write("musicgen_out.wav", 
				rate=music["sampling_rate"], 
				data=music["audio"])
