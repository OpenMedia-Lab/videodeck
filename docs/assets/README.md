# README assets

`readme-hero.svg` is an original workflow illustration. `readme-demo.gif` is an
actual 4.8–10.8 second excerpt from this repository's 12.4-second
[HyperFrames example](../../videodeck/assets/example/README.md), rendered locally
with its pinned dependencies. It contains no private voice, tutorial media or
account material. The example's audio is a generated continuity fixture; GIF has
no audio.

From the repository root, reproduce the source render using the example README,
then export the excerpt:

```sh
ffmpeg -ss 4.8 -t 6 -i videodeck/assets/example/renders/expert-routing.mp4 \
  -vf 'fps=12,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3' \
  -loop 0 /tmp/videodeck-readme-demo.gif
```

This demonstrates object continuity and a weighted-output mechanism, not a full
narration workflow or a universal visual template.
