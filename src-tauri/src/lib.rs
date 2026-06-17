use std::error::Error;

use anyhow::Result;
use tauri::App;

mod misc;
mod nbs;
// mod player;

use crate::nbs::{setup as setup_nbs, *};

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(
            tauri_plugin_log::Builder::new()
                .level(tauri_plugin_log::log::LevelFilter::Info)
                .build(),
        )
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![
            load_nbs_file,
            nbs_layer_names,
            notes_between_ticks
        ])
        .setup(setup)
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

fn setup(app: &mut App) -> Result<(), Box<dyn Error>> {
    setup_nbs(app)?;
    Ok(())
}
