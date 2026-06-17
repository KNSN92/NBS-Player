use std::{collections::HashMap, sync::RwLock};

use anyhow::Result;
use log::error;
use nbs_rust::{
    header::Header,
    io::NbsIOError,
    noteblock::{LayerId, Note},
    Nbs, Tick,
};
use tauri::{App, AppHandle, Manager};

use crate::hashmap;

pub struct LoadedNbs(pub Option<Nbs>);

pub fn setup(app: &mut App) -> Result<()> {
    app.manage(RwLock::new(LoadedNbs(None)));
    Ok(())
}

#[tauri::command]
pub async fn load_nbs_file(app_handle: AppHandle, path: String) -> Result<Header, String> {
    let loaded_nbs = app_handle.state::<RwLock<LoadedNbs>>();
    let nbs = Nbs::open(path);
    match nbs {
        Ok(nbs) => {
            let mut loaded_nbs = loaded_nbs.write().unwrap();
            let header = nbs.header.clone();
            *loaded_nbs = LoadedNbs(Some(nbs));
            Ok(header)
        }
        Err(NbsIOError::IOError(err)) => {
            error!("Failed to load NBS file: {}", err);
            Err("IOError".to_string())
        }
        Err(NbsIOError::UnsupportedVersion(version)) => {
            error!("Failed to load NBS file: Unsupported version {version}");
            Err("UnsupportedVersion".to_string())
        }
    }
}

#[tauri::command]
pub async fn nbs_layer_names(app_handle: AppHandle) -> Option<Vec<String>> {
    let loaded_nbs = app_handle.state::<RwLock<LoadedNbs>>();
    let loaded_nbs = loaded_nbs.read().unwrap();
    let nbs = loaded_nbs.0.as_ref()?;
    let names = nbs
        .note_blocks
        .layers()
        .iter()
        .map(|l| l.name.clone())
        .collect();
    Some(names)
}

#[tauri::command]
pub async fn notes_between_ticks(
    app_handle: AppHandle,
    start_tick: u32,
    end_tick: u32,
) -> Option<HashMap<Tick, Vec<(LayerId, Note)>>> {
    let loaded_nbs = app_handle.state::<RwLock<LoadedNbs>>();
    let loaded_nbs = loaded_nbs.read().unwrap();
    let nbs = loaded_nbs.0.as_ref()?;
    let mut notes = hashmap!();
    //TODO: optimize this by not iterating through all ticks, but only the ticks that have notes
    for tick in start_tick..=end_tick {
        if let Some(note_blocks) = nbs.note_blocks.notes_at_tick(tick) {
            let note_blocks = note_blocks
                .iter()
                .map(|(layer_id, note)| (*layer_id, *note))
                .collect();
            notes.insert(tick, note_blocks);
        }
    }
    Some(notes)
}
