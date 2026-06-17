import { Header } from "@/models/header";
import { NoteBlocks } from "@/models/noteblock";
import { invoke } from "@tauri-apps/api/core";

export type NbsIOError = "IOError" | "UnsupportedVersion";

export async function load_nbs_file(path: string): Promise<Header> {
  return invoke("load_nbs_file", { path });
}

export async function nbs_layer_names(): Promise<string[] | null> {
  return invoke("nbs_layer_names");
}

export async function notes_between_ticks(start_tick: number, end_tick: number): Promise<NoteBlocks | null> {
  return invoke("notes_between_ticks", { startTick: start_tick, endTick: end_tick });
}
