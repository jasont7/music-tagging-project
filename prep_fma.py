import os
import pandas as pd
import pydub

# select tracks from 'small' and 'medium' subsets
metadata_dir = '../A4/fma_metadata'
tracks = pd.read_csv(f'{metadata_dir}/tracks.csv', index_col=0, header=[0, 1])
small_med = tracks[tracks['set', 'subset'] >= 'medium']

print('tracks:', small_med.shape[0], '\n')
print(small_med['set', 'subset'].value_counts(), '\n')
print(small_med['track', 'genre_top'].value_counts(), '\n')


# Build fma_medium_trimmed dataset (same code as fma_smaller from A4)

input_dir = '../A4/fma_medium'
output_dir = 'fma_medium_trimmed'
os.makedirs(output_dir, exist_ok=True)

i = 0  # if the program crashes, change this to the last track that was being processed
skipped = 0

for idx, track in small_med[i:].iterrows():
    print(f'Processing track {i}/{len(small_med)} ({idx}), skipped {skipped}', end='\r')

    try:
        # construct the input file path based on the index (ID)
        input_subdir = str(idx).zfill(6)[:3]  # first three digits for the subdirectory
        input_filename = str(idx).zfill(6) + '.mp3'
        input_path = os.path.join(input_dir, input_subdir, input_filename)

        # load the mp3 file
        audio = pydub.AudioSegment.from_mp3(input_path)
        trimmed_audio = audio[:6000]  # trim to the first 6 seconds

        # save the trimmed audio file to disk
        genre = track['track', 'genre_top']
        genre_clean = ''.join([char.lower() for char in genre if char.isalpha()])
        output_subdir = os.path.join(output_dir, genre_clean)
        os.makedirs(output_subdir, exist_ok=True)
        output_filename = str(idx).zfill(6) + '.wav'
        output_path = os.path.join(output_subdir, output_filename)
        trimmed_audio.export(output_path, format='wav')
    except:
        skipped += 1

    i += 1
