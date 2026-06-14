# Note Atlas

This tool generates an atlas image of note blocks and its metadata for use in Nbs Player.
It generates the colors of the note blocks by blending the dye colors in Minecraft and the note block colors in NoteBlockStudio.
Also, several blend functions are provided, so you can choose and use your favorite blend function. (Some blend functions have strange behavior, but please forgive me~)
By specifying the seed value, you can generate the coloring of the note blocks in your favorite order.

Nbs Playerで使用するノートブロックのアトラス画像とそのメタデータを生成するツールです。
Minecraftの染料色とNoteBlockStudioのノートブロックの色を用意したので、これらをブレンドしてノートブロックの色を生成しています。
また、幾つかのブレンド関数を用意しているので、好みのブレンド関数を選択して使用することができます。(一部挙動が変なブレンド関数もあるけどご容赦ください〜)
また、シード値を指定する事で自分好みの並び順でノートブロックのカラーリングを生成することができます。

## Usage

You need to install uv beforehand

```bash
uv sync
uv run main.py
```
