"""
Table schemas for explicit-column SQLite tables.

Each schema is a dict mapping column_name -> "SQL_TYPE_DEFAULTS".
Special types:
  - JSON / JSON_LIST / JSON_DICT: auto-serialized to TEXT, auto-parsed on read
"""

# =============================================================================
# Profile tables — one row per (uid, game_version)
# All version fields become direct columns. uid-level IDs (iidx_id, etc.) are
# duplicated per row (denormalized) for simplicity.
# =============================================================================

IIDX_PROFILE = {
    "doc_id":          "INTEGER PRIMARY KEY AUTOINCREMENT",
    "uid": "INTEGER NOT NULL",
    "game_version":    "INTEGER NOT NULL DEFAULT 0",
    "iidx_id":         "INTEGER DEFAULT 0",
    # Basic profile
    "djname":          "INTEGER DEFAULT 0",
    "region":          "INTEGER DEFAULT 1",
    "pid":             "INTEGER DEFAULT 13",
    # Qpro customization
    "head":            "INTEGER DEFAULT 0",
    "hair":            "INTEGER DEFAULT 0",
    "face":            "INTEGER DEFAULT 0",
    "hand":            "INTEGER DEFAULT 0",
    "body":            "INTEGER DEFAULT 0",
    "frame":           "INTEGER DEFAULT 0",
    "turntable":       "INTEGER DEFAULT 0",
    "explosion":       "INTEGER DEFAULT 0",
    "bgm":             "INTEGER DEFAULT 0",
    "folder_mask":     "INTEGER DEFAULT 0",
    # Display options SP
    "d_hispeed":       "REAL DEFAULT 0.0",
    "d_notes":         "REAL DEFAULT 0.0",
    "d_sdlen":         "INTEGER DEFAULT 0",
    "d_sdtype":        "INTEGER DEFAULT 0",
    "d_sorttype":      "INTEGER DEFAULT 0",
    "d_gno":           "INTEGER DEFAULT 0",
    "d_sub_gno":       "INTEGER DEFAULT 0",
    "d_gtype":         "INTEGER DEFAULT 0",
    "d_graph_score":   "INTEGER DEFAULT 0",
    "d_exscore":       "INTEGER DEFAULT 0",
    "d_judge":         "INTEGER DEFAULT 0",
    "d_judgeAdj":      "INTEGER DEFAULT 0",
    "d_timing":        "INTEGER DEFAULT 0",
    "d_tune":          "INTEGER DEFAULT 0",
    "d_liflen":        "INTEGER DEFAULT 0",
    "d_lane_brignt":   "INTEGER DEFAULT 0",
    "d_disp_judge":    "INTEGER DEFAULT 0",
    "d_gauge_disp":    "INTEGER DEFAULT 0",
    "d_ghost_score":   "INTEGER DEFAULT 0",
    "d_opstyle":       "INTEGER DEFAULT 0",
    "d_pace":          "INTEGER DEFAULT 0",
    "d_tsujigiri_disp":"INTEGER DEFAULT 0",
    "d_auto_adjust":   "INTEGER DEFAULT 0",
    "d_auto_scrach":   "INTEGER DEFAULT 0",
    "d_camera_layout": "INTEGER DEFAULT 0",
    "d_classic_hispeed": "INTEGER DEFAULT 0",
    "d_timing_split": "INTEGER DEFAULT 0",
    "d_visualization": "INTEGER DEFAULT 0",
    "hide_name": "INTEGER DEFAULT 0",
    "s_auto_adjust": "INTEGER DEFAULT 0",
    "s_auto_scrach": "INTEGER DEFAULT 0",
    "s_camera_layout": "INTEGER DEFAULT 0",
    "s_classic_hispeed": "INTEGER DEFAULT 0",
    "s_disp_judge": "INTEGER DEFAULT 0",
    "s_exscore": "INTEGER DEFAULT 0",
    "s_gauge_disp": "INTEGER DEFAULT 0",
    "s_ghost_score": "INTEGER DEFAULT 0",
    "s_gno": "INTEGER DEFAULT 0",
    "s_graph_score": "INTEGER DEFAULT 0",
    "s_gtype": "INTEGER DEFAULT 0",
    "s_hispeed": "REAL DEFAULT 0.0",
    "s_judge": "INTEGER DEFAULT 0",
    "s_judgeAdj": "INTEGER DEFAULT 0",
    "s_lane_brignt": "INTEGER DEFAULT 0",
    "s_liflen": "INTEGER DEFAULT 0",
    "s_notes": "REAL DEFAULT 0.0",
    "s_opstyle": "INTEGER DEFAULT 0",
    "s_pace": "INTEGER DEFAULT 0",
    "s_sdlen": "INTEGER DEFAULT 0",
    "s_sdtype": "INTEGER DEFAULT 0",
    "s_sorttype": "INTEGER DEFAULT 0",
    "s_sub_gno": "INTEGER DEFAULT 0",
    "s_timing": "INTEGER DEFAULT 0",
    "s_timing_split": "INTEGER DEFAULT 0",
    "s_tsujigiri_disp": "INTEGER DEFAULT 0",
    "s_tune": "INTEGER DEFAULT 0",
    "s_visualization": "INTEGER DEFAULT 0",
    "stepup_dp_fluctuation": "INTEGER DEFAULT 0",
    "stepup_sp_fluctuation": "INTEGER DEFAULT 0",
    "gno": "INTEGER DEFAULT 0",
    "help": "INTEGER DEFAULT 0",
    "hispeed": "REAL DEFAULT 0.0",
    "judge": "INTEGER DEFAULT 0",
    "judgeAdj": "INTEGER DEFAULT 0",
    "lift": "INTEGER DEFAULT 0",
    "notes": "REAL DEFAULT 0.0",
    "opstyle": "INTEGER DEFAULT 0",
    "pase": "INTEGER DEFAULT 0",
    "sdhd": "INTEGER DEFAULT 0",
    "sdtype": "INTEGER DEFAULT 0",
    "timing": "INTEGER DEFAULT 0",
    "d_classic_hispeed": "INTEGER DEFAULT 0",
    "d_timing_split": "INTEGER DEFAULT 0",
    "d_visualization": "INTEGER DEFAULT 0",
    "hide_name": "INTEGER DEFAULT 0",
    "s_auto_adjust": "INTEGER DEFAULT 0",
    "s_auto_scrach": "INTEGER DEFAULT 0",
    "s_camera_layout": "INTEGER DEFAULT 0",
    "s_classic_hispeed": "INTEGER DEFAULT 0",
    "s_disp_judge": "INTEGER DEFAULT 0",
    "s_exscore": "INTEGER DEFAULT 0",
    "s_gauge_disp": "INTEGER DEFAULT 0",
    "s_ghost_score": "INTEGER DEFAULT 0",
    "s_gno": "INTEGER DEFAULT 0",
    "s_graph_score": "INTEGER DEFAULT 0",
    "s_gtype": "INTEGER DEFAULT 0",
    "s_hispeed": "REAL DEFAULT 0.0",
    "s_judge": "INTEGER DEFAULT 0",
    "s_judgeAdj": "INTEGER DEFAULT 0",
    "s_lane_brignt": "INTEGER DEFAULT 0",
    "s_liflen": "INTEGER DEFAULT 0",
    "s_notes": "REAL DEFAULT 0.0",
    "s_opstyle": "INTEGER DEFAULT 0",
    "s_pace": "INTEGER DEFAULT 0",
    "s_sdlen": "INTEGER DEFAULT 0",
    "s_sdtype": "INTEGER DEFAULT 0",
    "s_sorttype": "INTEGER DEFAULT 0",
    "s_sub_gno": "INTEGER DEFAULT 0",
    "s_timing": "INTEGER DEFAULT 0",
    "s_timing_split": "INTEGER DEFAULT 0",
    "s_tsujigiri_disp": "INTEGER DEFAULT 0",
    "s_tune": "INTEGER DEFAULT 0",
    "s_visualization": "INTEGER DEFAULT 0",
    "stepup_dp_fluctuation": "INTEGER DEFAULT 0",
    "stepup_sp_fluctuation": "INTEGER DEFAULT 0",
    "gno": "INTEGER DEFAULT 0",
    "help": "INTEGER DEFAULT 0",
    "hispeed": "REAL DEFAULT 0.0",
    "judge": "INTEGER DEFAULT 0",
    "judgeAdj": "INTEGER DEFAULT 0",
    "lift": "INTEGER DEFAULT 0",
    "notes": "REAL DEFAULT 0.0",
    "opstyle": "INTEGER DEFAULT 0",
    "pase": "INTEGER DEFAULT 0",
    "sdhd": "INTEGER DEFAULT 0",
    "sdtype": "INTEGER DEFAULT 0",
    "timing": "INTEGER DEFAULT 0",
    # Display options DP
    "dp_opt":          "INTEGER DEFAULT 0",
    "dp_opt2":         "INTEGER DEFAULT 0",
    # Options
    "sudden":          "INTEGER DEFAULT 0",
    "judge_pos":       "INTEGER DEFAULT 0",
    "categoryvoice":   "INTEGER DEFAULT 0",
    "note":            "INTEGER DEFAULT 0",
    "fullcombo":       "INTEGER DEFAULT 0",
    "keybeam":         "INTEGER DEFAULT 0",
    "judgestring":     "INTEGER DEFAULT 0",
    "soundpreview":    "INTEGER DEFAULT 0",
    "grapharea":       "INTEGER DEFAULT 0",
    "effector_lock":   "INTEGER DEFAULT 0",
    "effector_type":   "INTEGER DEFAULT 0",
    "explosion_size":  "INTEGER DEFAULT 0",
    "alternate_hcn":   "INTEGER DEFAULT 0",
    "kokokara_start":  "INTEGER DEFAULT 0",
    "dach":            "INTEGER DEFAULT 0",
    "gpos":            "INTEGER DEFAULT 0",
    "mode":            "INTEGER DEFAULT 0",
    "ngrade":          "INTEGER DEFAULT 0",
    "pmode":           "INTEGER DEFAULT 0",
    "rtype":           "INTEGER DEFAULT 0",
    "sach":            "INTEGER DEFAULT 0",
    "sp_opt":          "INTEGER DEFAULT 0",
    "spnum":           "INTEGER DEFAULT 0",
    "dpnum":           "INTEGER DEFAULT 0",
    "deller":          "INTEGER DEFAULT 0",
    # Language / movie
    "language_setting":"INTEGER DEFAULT 0",
    "movie_agreement": "INTEGER DEFAULT 0",
    # Grades
    "grade_single":    "INTEGER DEFAULT -1",
    "grade_double":    "INTEGER DEFAULT -1",
    "grade_values": "JSON_LIST",
    # DJ rank
    "dj_rank_single_rank": "JSON_LIST",
    "dj_rank_double_rank": "JSON_LIST",
    "dj_rank_single_point": "JSON_LIST",
    "dj_rank_double_point": "JSON_LIST",
    # Notes radar
    "notes_radar_single": "JSON_LIST",
    "notes_radar_double": "JSON_LIST",
    # Achievements
    "achievements_trophy": "JSON_LIST",
    "achievements_last_weekly":    "INTEGER DEFAULT 0",
    "achievements_pack_comp":      "INTEGER DEFAULT 0",
    "achievements_pack_flg":       "INTEGER DEFAULT 0",
    "achievements_pack_id":        "INTEGER DEFAULT 0",
    "achievements_play_pack":      "INTEGER DEFAULT 0",
    "achievements_visit_flg":      "INTEGER DEFAULT 0",
    "achievements_weekly_num":     "INTEGER DEFAULT 0",
    # Step-up
    "stepup_dp_level":             "INTEGER DEFAULT 0",
    "stepup_dp_mplay":             "INTEGER DEFAULT 0",
    "stepup_enemy_damage":         "INTEGER DEFAULT 0",
    "stepup_enemy_defeat_flg":     "INTEGER DEFAULT 0",
    "stepup_mission_clear_num":    "INTEGER DEFAULT 0",
    "stepup_progress":             "INTEGER DEFAULT 0",
    "stepup_sp_level":             "INTEGER DEFAULT 0",
    "stepup_sp_mplay":             "INTEGER DEFAULT 0",
    "stepup_tips_read_list":       "INTEGER DEFAULT 0",
    "stepup_total_point":          "INTEGER DEFAULT 0",
    "stepup_is_track_ticket":      "INTEGER DEFAULT 0",
    # Lightning model
    "lightning_play_data_spnum":   "INTEGER DEFAULT 0",
    "lightning_play_data_dpnum":   "INTEGER DEFAULT 0",
    "lightning_setting_slider": "JSON_LIST",
    "lightning_setting_light": "JSON_LIST",
    "lightning_setting_concentration":     "INTEGER DEFAULT 0",
    "lightning_setting_headphone_vol":     "INTEGER DEFAULT 0",
    "lightning_setting_resistance_sp_left": "INTEGER DEFAULT 0",
    "lightning_setting_resistance_sp_right":"INTEGER DEFAULT 0",
    "lightning_setting_resistance_dp_left": "INTEGER DEFAULT 0",
    "lightning_setting_resistance_dp_right":"INTEGER DEFAULT 0",
    "lightning_setting_skin_0":            "INTEGER DEFAULT 0",
    "lightning_setting_flg_skin_0":        "INTEGER DEFAULT 0",
    # Event
    "event_1_story_prog":               "INTEGER DEFAULT 0",
    "event_1_last_select_area":          "INTEGER DEFAULT 0",
    "event_1_failed_num":                "INTEGER DEFAULT 0",
    "event_1_event_play_num":            "INTEGER DEFAULT 0",
    "event_1_last_select_area_id":       "INTEGER DEFAULT 0",
    "event_1_last_select_platform_type": "INTEGER DEFAULT 0",
    "event_1_last_select_platform_id":   "INTEGER DEFAULT 0",
    # Web UI options (underscore prefix)
    "_show_category_grade":           "INTEGER DEFAULT 0",
    "_show_category_status":          "INTEGER DEFAULT 1",
    "_show_category_difficulty":      "INTEGER DEFAULT 1",
    "_show_category_alphabet":        "INTEGER DEFAULT 1",
    "_show_category_rival_play":      "INTEGER DEFAULT 0",
    "_show_category_rival_winlose":   "INTEGER DEFAULT 1",
    "_show_category_all_rival_play":  "INTEGER DEFAULT 0",
    "_show_category_arena_winlose":   "INTEGER DEFAULT 1",
    "_show_rival_shop_info":          "INTEGER DEFAULT 1",
    "_hide_play_count":               "INTEGER DEFAULT 0",
    "_show_score_graph_cutin":        "INTEGER DEFAULT 1",
    "_hide_iidx_id":                  "INTEGER DEFAULT 0",
    "_classic_hispeed":               "INTEGER DEFAULT 0",
    "_beginner_option_swap":          "INTEGER DEFAULT 1",
    "_show_lamps_as_no_play_in_arena":"INTEGER DEFAULT 0",
    # Skin customize
    "skin_customize_flag_frame":      "INTEGER DEFAULT 0",
    "skin_customize_flag_bgm":        "INTEGER DEFAULT 0",
    "skin_customize_flag_lane":       "INTEGER DEFAULT 0",
    # Rivals
    "sp_rival_1_iidx_id":  "INTEGER DEFAULT 0",
    "sp_rival_2_iidx_id":  "INTEGER DEFAULT 0",
    "sp_rival_3_iidx_id":  "INTEGER DEFAULT 0",
    "sp_rival_4_iidx_id":  "INTEGER DEFAULT 0",
    "sp_rival_5_iidx_id":  "INTEGER DEFAULT 0",
    "sp_rival_6_iidx_id":  "INTEGER DEFAULT 0",
    "dp_rival_1_iidx_id":  "INTEGER DEFAULT 0",
    "dp_rival_2_iidx_id":  "INTEGER DEFAULT 0",
    "dp_rival_3_iidx_id":  "INTEGER DEFAULT 0",
    "dp_rival_4_iidx_id":  "INTEGER DEFAULT 0",
    "dp_rival_5_iidx_id":  "INTEGER DEFAULT 0",
    "dp_rival_6_iidx_id":  "INTEGER DEFAULT 0",
    # Misc list fields
    "params": "JSON_LIST",
    "items": "JSON_LIST",
}


# =============================================================================
# IIDX scores — play log, append only
# =============================================================================

IIDX_SCORES = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "timestamp":    "REAL DEFAULT 0.0",
    "game_version": "INTEGER DEFAULT 0",
    "iidx_id":      "INTEGER DEFAULT 0",
    "pid":          "INTEGER DEFAULT 0",
    "clear_flg":    "INTEGER DEFAULT 0",
    "is_death":     "INTEGER DEFAULT 0",
    "music_id":     "INTEGER DEFAULT 0",
    "play_style":   "INTEGER DEFAULT 0",
    "chart_id":     "INTEGER DEFAULT 0",
    "pgreat_num":   "INTEGER DEFAULT 0",
    "great_num":    "INTEGER DEFAULT 0",
    "ex_score":     "INTEGER DEFAULT 0",
    "miss_count":   "INTEGER DEFAULT 0",
    "folder_type":  "INTEGER DEFAULT 0",
    "gauge_type":   "INTEGER DEFAULT 0",
    "graph_type":   "INTEGER DEFAULT 0",
    "mode_type":    "INTEGER DEFAULT 0",
    "option1":      "INTEGER DEFAULT 0",
    "option2":      "INTEGER DEFAULT 0",
    "ghost":        "INTEGER DEFAULT 0",
    "ghost_gauge":  "INTEGER DEFAULT 0",
}

# =============================================================================
# IIDX best scores — upserted, per player per chart
# =============================================================================

IIDX_SCORES_BEST = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "game_version": "INTEGER DEFAULT 0",
    "iidx_id":      "INTEGER DEFAULT 0",
    "pid":          "INTEGER DEFAULT 0",
    "play_style":   "INTEGER DEFAULT 0",
    "music_id":     "INTEGER DEFAULT 0",
    "chart_id":     "INTEGER DEFAULT 0",
    "miss_count":   "INTEGER DEFAULT -1",
    "ex_score":     "INTEGER DEFAULT 0",
    "ghost":        "INTEGER DEFAULT 0",
    "ghost_gauge":  "INTEGER DEFAULT 0",
    "clear_flg":    "INTEGER DEFAULT 0",
    "gauge_type":   "INTEGER DEFAULT 4",
}

# =============================================================================
# IIDX score stats — server-wide aggregates per chart
# =============================================================================

IIDX_SCORE_STATS = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "game_version": "INTEGER DEFAULT 0",
    "play_style":   "INTEGER DEFAULT 0",
    "music_id":     "INTEGER DEFAULT 0",
    "chart_id":     "INTEGER DEFAULT 0",
    "play_count":   "INTEGER DEFAULT 0",
    "fc_count":     "INTEGER DEFAULT 0",
    "clear_count":  "INTEGER DEFAULT 0",
    "fc_rate":      "INTEGER DEFAULT 0",
    "clear_rate":   "INTEGER DEFAULT 0",
}

# =============================================================================
# IIDX class — play log for dan courses
# =============================================================================

IIDX_CLASS = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "timestamp":    "REAL DEFAULT 0.0",
    "game_version": "INTEGER DEFAULT 0",
    "iidx_id":      "INTEGER DEFAULT 0",
    "achi":         "INTEGER DEFAULT 0",
    "cstage":       "INTEGER DEFAULT 0",
    "gid":          "INTEGER DEFAULT 0",
    "gtype":        "INTEGER DEFAULT 0",
    "is_ex":        "INTEGER DEFAULT 0",
    "is_mirror":    "INTEGER DEFAULT 0",
}

# =============================================================================
# IIDX class best — personal best per course
# =============================================================================

IIDX_CLASS_BEST = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "game_version": "INTEGER DEFAULT 0",
    "iidx_id":      "INTEGER DEFAULT 0",
    "achi":         "INTEGER DEFAULT 0",
    "cstage":       "INTEGER DEFAULT 0",
    "gid":          "INTEGER DEFAULT 0",
    "gtype":        "INTEGER DEFAULT 0",
    "is_ex":        "INTEGER DEFAULT 0",
    "is_mirror":    "INTEGER DEFAULT 0",
}

# =============================================================================
# DDR profile
# =============================================================================

DDR_PROFILE = {
    "doc_id":            "INTEGER PRIMARY KEY AUTOINCREMENT",
    "uid": "INTEGER NOT NULL",
    "game_version":      "INTEGER NOT NULL DEFAULT 0",
    "ddr_id":            "INTEGER DEFAULT 0",
    # Per-version fields
    "calories_disp":     "TEXT DEFAULT 'Off'",
    "character":         "TEXT DEFAULT 'All Character Random'",
    "arrow_skin":        "TEXT DEFAULT 'Normal'",
    "filter":            "TEXT DEFAULT 'Off'",
    "guideline":         "TEXT DEFAULT 'Off'",
    "priority":          "TEXT DEFAULT 'Judgment'",
    "timing_disp":       "TEXT DEFAULT 'On'",
    "common":            "INTEGER DEFAULT 0",
    "option":            "INTEGER DEFAULT 0",
    "last":              "INTEGER DEFAULT 0",
    "rival":             "INTEGER DEFAULT 0",
    "rival_1_ddr_id":    "INTEGER DEFAULT 0",
    "rival_2_ddr_id":    "INTEGER DEFAULT 0",
    "rival_3_ddr_id":    "INTEGER DEFAULT 0",
    "single_grade":      "INTEGER DEFAULT 0",
    "double_grade":      "INTEGER DEFAULT 0",
    "common_dancername": "INTEGER DEFAULT 0",
    "common_area":       "INTEGER DEFAULT 13",
    "grade_values": "JSON_LIST",
    "customize": "JSON_DICT",
    "params": "JSON_LIST",
}

# =============================================================================
# DDR scores — play log
# =============================================================================

DDR_SCORES = {
    "doc_id":            "INTEGER PRIMARY KEY AUTOINCREMENT",
    "timestamp":         "REAL DEFAULT 0.0",
    "pcbid":             "INTEGER DEFAULT 0",
    "shoparea":          "INTEGER DEFAULT 0",
    "game_version":      "INTEGER DEFAULT 0",
    "ddr_id":            "INTEGER DEFAULT 0",
    "playstyle":         "INTEGER DEFAULT 0",
    "mcode":             "INTEGER DEFAULT 0",
    "difficulty":        "INTEGER DEFAULT 0",
    "rank":              "INTEGER DEFAULT 0",
    "lamp":              "INTEGER DEFAULT 0",
    "score":             "INTEGER DEFAULT 0",
    "exscore":           "INTEGER DEFAULT 0",
    "maxcombo":          "INTEGER DEFAULT 0",
    "life":              "INTEGER DEFAULT 0",
    "fastcount":         "INTEGER DEFAULT 0",
    "slowcount":         "INTEGER DEFAULT 0",
    "judge_marvelous":   "INTEGER DEFAULT 0",
    "judge_perfect":     "INTEGER DEFAULT 0",
    "judge_great":       "INTEGER DEFAULT 0",
    "judge_good":        "INTEGER DEFAULT 0",
    "judge_boo":         "INTEGER DEFAULT 0",
    "judge_miss":        "INTEGER DEFAULT 0",
    "judge_ok":          "INTEGER DEFAULT 0",
    "judge_ng":          "INTEGER DEFAULT 0",
    "calorie":           "INTEGER DEFAULT 0",
    "ghostsize":         "INTEGER DEFAULT 0",
    "ghost":             "INTEGER DEFAULT 0",
    "opt_speed":         "INTEGER DEFAULT 0",
    "opt_boost":         "INTEGER DEFAULT 0",
    "opt_appearance":    "INTEGER DEFAULT 0",
    "opt_turn":          "INTEGER DEFAULT 0",
    "opt_dark":          "INTEGER DEFAULT 0",
    "opt_scroll":        "INTEGER DEFAULT 0",
    "opt_arrowcolor":    "INTEGER DEFAULT 0",
    "opt_cut":           "INTEGER DEFAULT 0",
    "opt_freeze":        "INTEGER DEFAULT 0",
    "opt_jump":          "INTEGER DEFAULT 0",
    "opt_arrowshape":    "INTEGER DEFAULT 0",
    "opt_filter":        "INTEGER DEFAULT 0",
    "opt_guideline":     "INTEGER DEFAULT 0",
    "opt_gauge":         "INTEGER DEFAULT 0",
    "opt_judgepriority": "INTEGER DEFAULT 0",
    "opt_timing":        "INTEGER DEFAULT 0",
    "flare_force":       "INTEGER DEFAULT 0",
}

# =============================================================================
# DDR scores best — personal best per chart
# =============================================================================

DDR_SCORES_BEST = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "game_version": "INTEGER DEFAULT 0",
    "ddr_id":       "INTEGER DEFAULT 0",
    "playstyle":    "INTEGER DEFAULT 0",
    "mcode":        "INTEGER DEFAULT 0",
    "difficulty":   "INTEGER DEFAULT 0",
    "rank":         "INTEGER DEFAULT 100",
    "lamp":         "INTEGER DEFAULT 0",
    "score":        "INTEGER DEFAULT 0",
    "exscore":      "INTEGER DEFAULT 0",
    "ghostid":      "INTEGER DEFAULT -1",
    "flare_force":  "INTEGER DEFAULT 0",
}

# =============================================================================
# SDVX profile
# =============================================================================

SDVX_PROFILE = {
    "doc_id":               "INTEGER PRIMARY KEY AUTOINCREMENT",
    "uid": "INTEGER NOT NULL",
    "game_version":         "INTEGER NOT NULL DEFAULT 0",
    "sdvx_id":              "INTEGER DEFAULT 0",
    "name":                 "INTEGER DEFAULT 0",
    "appeal_id":            "INTEGER DEFAULT 0",
    "skill_level":          "INTEGER DEFAULT 0",
    "skill_base_id":        "INTEGER DEFAULT 0",
    "skill_name_id":        "INTEGER DEFAULT 0",
    "earned_gamecoin_packet":"INTEGER DEFAULT 0",
    "earned_gamecoin_block": "INTEGER DEFAULT 0",
    "earned_blaster_energy": "INTEGER DEFAULT 0",
    "earned_extrack_energy": "INTEGER DEFAULT 0",
    "used_packet_booster":   "INTEGER DEFAULT 0",
    "used_block_booster":    "INTEGER DEFAULT 0",
    "hispeed":              "INTEGER DEFAULT 0",
    "lanespeed":            "INTEGER DEFAULT 0",
    "gauge_option":         "INTEGER DEFAULT 0",
    "ars_option":           "INTEGER DEFAULT 0",
    "notes_option":         "INTEGER DEFAULT 0",
    "early_late_disp":      "INTEGER DEFAULT 0",
    "draw_adjust":          "INTEGER DEFAULT 0",
    "eff_c_left":           "INTEGER DEFAULT 0",
    "eff_c_right":          "INTEGER DEFAULT 1",
    "music_id":             "INTEGER DEFAULT 0",
    "music_type":           "INTEGER DEFAULT 0",
    "sort_type":            "INTEGER DEFAULT 0",
    "narrow_down":          "INTEGER DEFAULT 0",
    "headphone":            "INTEGER DEFAULT 1",
    "print_count":          "INTEGER DEFAULT 0",
    "start_option":         "INTEGER DEFAULT 0",
    "bgm":                  "INTEGER DEFAULT 0",
    "submonitor":           "INTEGER DEFAULT 0",
    "nemsys":               "INTEGER DEFAULT 0",
    "stampA":               "INTEGER DEFAULT 0",
    "stampB":               "INTEGER DEFAULT 0",
    "stampC":               "INTEGER DEFAULT 0",
    "stampD":               "INTEGER DEFAULT 0",
    "items": "JSON_LIST",
    "params": "JSON_LIST",
}

# =============================================================================
# SDVX scores
# =============================================================================

SDVX_SCORES = {
    "doc_id":         "INTEGER PRIMARY KEY AUTOINCREMENT",
    "timestamp":      "REAL DEFAULT 0.0",
    "game_version":   "INTEGER DEFAULT 0",
    "sdvx_id":        "INTEGER DEFAULT 0",
    "play_id":        "INTEGER DEFAULT 0",
    "music_id":       "INTEGER DEFAULT 0",
    "music_type":     "INTEGER DEFAULT 0",
    "score":          "INTEGER DEFAULT 0",
    "exscore":        "INTEGER DEFAULT 0",
    "clear_type":     "INTEGER DEFAULT 0",
    "score_grade":    "INTEGER DEFAULT 0",
    "max_chain":      "INTEGER DEFAULT 0",
    "just":           "INTEGER DEFAULT 0",
    "critical":       "INTEGER DEFAULT 0",
    "near":           "INTEGER DEFAULT 0",
    "error":          "INTEGER DEFAULT 0",
    "effective_rate": "INTEGER DEFAULT 0",
    "btn_rate":       "INTEGER DEFAULT 0",
    "long_rate":      "INTEGER DEFAULT 0",
    "vol_rate":       "INTEGER DEFAULT 0",
    "mode":           "INTEGER DEFAULT 0",
    "gauge_type":     "INTEGER DEFAULT 0",
    "notes_option":   "INTEGER DEFAULT 0",
    "online_num":     "INTEGER DEFAULT 0",
    "local_num":      "INTEGER DEFAULT 0",
    "challenge_type": "INTEGER DEFAULT 0",
    "retry_cnt":      "INTEGER DEFAULT 0",
    "judge": "JSON_LIST",
}

# =============================================================================
# SDVX scores best
# =============================================================================

SDVX_SCORES_BEST = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "game_version": "INTEGER DEFAULT 0",
    "sdvx_id":      "INTEGER DEFAULT 0",
    "name":         "INTEGER DEFAULT 0",
    "music_id":     "INTEGER DEFAULT 0",
    "music_type":   "INTEGER DEFAULT 0",
    "score":        "INTEGER DEFAULT 0",
    "exscore":      "INTEGER DEFAULT 0",
    "clear_type":   "INTEGER DEFAULT 0",
    "score_grade":  "INTEGER DEFAULT 0",
    "btn_rate":     "INTEGER DEFAULT 0",
    "long_rate":    "INTEGER DEFAULT 0",
    "vol_rate":     "INTEGER DEFAULT 0",
}

# =============================================================================
# DRS (Dancerush) profile
# =============================================================================

DRS_PROFILE = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "uid": "INTEGER NOT NULL",
    "game_version": "INTEGER NOT NULL DEFAULT 0",
    "drs_id":       "INTEGER DEFAULT 0",
    "name":         "INTEGER DEFAULT 0",
    "mode_id":      "INTEGER DEFAULT 0",
    "music_id":     "INTEGER DEFAULT 1",
    "music_type":   "TEXT DEFAULT '1a'",
    "params": "JSON_LIST",
}

# =============================================================================
# DRS scores
# =============================================================================

DRS_SCORES = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "timestamp":    "REAL DEFAULT 0.0",
    "game_version": "INTEGER DEFAULT 0",
    "drs_id":       "INTEGER DEFAULT 0",
    "music_id":     "INTEGER DEFAULT 0",
    "music_type":   "INTEGER DEFAULT 0",
    "mode":         "INTEGER DEFAULT 0",
    "score":        "INTEGER DEFAULT 0",
    "rank":         "INTEGER DEFAULT 0",
    "combo":        "INTEGER DEFAULT 0",
    "param":        "INTEGER DEFAULT 0",
    "perfect":      "INTEGER DEFAULT 0",
    "great":        "INTEGER DEFAULT 0",
    "good":         "INTEGER DEFAULT 0",
    "bad":          "INTEGER DEFAULT 0",
}

# =============================================================================
# DRS scores best
# =============================================================================

DRS_SCORES_BEST = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "game_version": "INTEGER DEFAULT 0",
    "drs_id":       "INTEGER DEFAULT 0",
    "name":         "INTEGER DEFAULT 0",
    "music_id":     "INTEGER DEFAULT 0",
    "music_type":   "INTEGER DEFAULT 0",
    "score":        "INTEGER DEFAULT 0",
    "rank":         "INTEGER DEFAULT 0",
    "combo":        "INTEGER DEFAULT 0",
    "param":        "INTEGER DEFAULT 0",
}

# =============================================================================
# Nostalgia profile
# =============================================================================

NOSTALGIA_PROFILE = {
    "doc_id":            "INTEGER PRIMARY KEY AUTOINCREMENT",
    "uid": "INTEGER NOT NULL",
    "game_version":      "INTEGER NOT NULL DEFAULT 0",
    "nostalgia_id":      "INTEGER DEFAULT 0",
    "name":              "INTEGER DEFAULT 0",
    "music_group":       "INTEGER DEFAULT 0",
    "music_index":       "INTEGER DEFAULT 0",
    "sheet_type":        "INTEGER DEFAULT 0",
    "perform_type":      "INTEGER DEFAULT 0",
    "filter_flag":       "INTEGER DEFAULT 0",
    "brooch_index":      "INTEGER DEFAULT 0",
    "hi_speed_level":    "INTEGER DEFAULT 0",
    "beat_guide":        "INTEGER DEFAULT 0",
    "headphone_volume":  "INTEGER DEFAULT 0",
    "judge_bar_pos":     "INTEGER DEFAULT 250",
    "hands_mode":        "INTEGER DEFAULT 0",
    "near_setting":      "INTEGER DEFAULT 0",
    "judge_delay_offset":"INTEGER DEFAULT 0",
    "key_beam_level":    "INTEGER DEFAULT 0",
    "orbit_type":        "INTEGER DEFAULT 0",
    "note_height":       "INTEGER DEFAULT 10",
    "note_width":        "INTEGER DEFAULT 10",
    "judge_width_type":  "INTEGER DEFAULT 10",
    "beat_guide_volume": "INTEGER DEFAULT 0",
    "beat_guide_type":   "INTEGER DEFAULT 0",
    "key_volume_offset": "INTEGER DEFAULT 0",
    "bgm_volume_offset": "INTEGER DEFAULT 0",
    "note_disp_type":    "INTEGER DEFAULT 0",
    "slow_fast":         "INTEGER DEFAULT 0",
    "option_setting":    "INTEGER DEFAULT 0",
    "judge_effect_adjust":"INTEGER DEFAULT 0",
    "simple_bg":         "INTEGER DEFAULT 0",
    "bingo_index":       "INTEGER DEFAULT 0",
    "class_basic":       "INTEGER DEFAULT 0",
    "class_recital":     "INTEGER DEFAULT 0",
    "grade_basic":       "INTEGER DEFAULT 0",
    "grade_recital":     "INTEGER DEFAULT 0",
    "money":             "INTEGER DEFAULT 0",
    "pianist_power":     "INTEGER DEFAULT 0",
    "fame_index":        "INTEGER DEFAULT 0",
    "kingdom_id":        "INTEGER DEFAULT 0",
    "quest_index":       "INTEGER DEFAULT 0",
    "param1": "JSON_LIST",
    "param2": "JSON_LIST",
}

# =============================================================================
# Nostalgia scores
# =============================================================================

NOSTALGIA_SCORES = {
    "doc_id":                              "INTEGER PRIMARY KEY AUTOINCREMENT",
    "timestamp":                           "REAL DEFAULT 0.0",
    "game_version":                        "INTEGER DEFAULT 0",
    "nostalgia_id":                        "INTEGER DEFAULT 0",
    "music_index":                         "INTEGER DEFAULT 0",
    "sheet_type":                          "INTEGER DEFAULT 0",
    "score":                               "INTEGER DEFAULT 0",
    "combo":                               "INTEGER DEFAULT 0",
    "grade":                               "INTEGER DEFAULT 0",
    "hands_mode":                          "INTEGER DEFAULT 0",
    "play_count":                          "INTEGER DEFAULT 0",
    "clear_count":                         "INTEGER DEFAULT 0",
    "multi_count":                         "INTEGER DEFAULT 0",
    "clear_flag":                          "INTEGER DEFAULT 0",
    "slow_count":                          "INTEGER DEFAULT 0",
    "fast_count":                          "INTEGER DEFAULT 0",
    "judge_count_miss":                    "INTEGER DEFAULT 0",
    "judge_count_good":                    "INTEGER DEFAULT 0",
    "judge_count_just":                    "INTEGER DEFAULT 0",
    "judge_count_super_just":              "INTEGER DEFAULT 0",
    "judge_count_near":                    "INTEGER DEFAULT 0",
    "judge_percent_max_count_long_miss":   "INTEGER DEFAULT 0",
    "judge_percent_max_count_long_good":   "INTEGER DEFAULT 0",
    "judge_percent_max_count_long_just":   "INTEGER DEFAULT 0",
    "judge_percent_max_count_long_super_just":"INTEGER DEFAULT 0",
    "judge_percent_max_count_long_near":   "INTEGER DEFAULT 0",
    "judge_percent_max_count_trill_miss":  "INTEGER DEFAULT 0",
    "judge_percent_max_count_trill_good":  "INTEGER DEFAULT 0",
    "judge_percent_max_count_trill_just":  "INTEGER DEFAULT 0",
    "judge_percent_max_count_trill_super_just":"INTEGER DEFAULT 0",
    "judge_percent_max_count_trill_near":  "INTEGER DEFAULT 0",
    "note_num_normal":                     "INTEGER DEFAULT 0",
    "note_num_long":                       "INTEGER DEFAULT 0",
    "note_num_glissando":                  "INTEGER DEFAULT 0",
    "note_num_trill":                      "INTEGER DEFAULT 0",
    "note_success_rate_normal":            "INTEGER DEFAULT 0",
    "note_success_rate_long":              "INTEGER DEFAULT 0",
    "note_success_rate_glissando":         "INTEGER DEFAULT 0",
    "note_success_rate_trill":             "INTEGER DEFAULT 0",
    "best_score":                          "INTEGER DEFAULT 0",
}

# =============================================================================
# Nostalgia scores best
# =============================================================================

NOSTALGIA_SCORES_BEST = {
    "doc_id":       "INTEGER PRIMARY KEY AUTOINCREMENT",
    "game_version": "INTEGER DEFAULT 0",
    "nostalgia_id": "INTEGER DEFAULT 0",
    "music_index":  "INTEGER DEFAULT 0",
    "sheet_type":   "INTEGER DEFAULT 0",
    "score":        "INTEGER DEFAULT 0",
    "play_count":   "INTEGER DEFAULT 0",
    "clear_count":  "INTEGER DEFAULT 0",
    "multi_count":  "INTEGER DEFAULT 0",
    "clear_flag":   "INTEGER DEFAULT 0",
    "hands_mode":   "INTEGER DEFAULT 0",
    "grade":        "INTEGER DEFAULT 0",
}

# =============================================================================
# Gitadora profile
# =============================================================================

GITADORA_PROFILE = {
    "doc_id":                     "INTEGER PRIMARY KEY AUTOINCREMENT",
    "uid": "INTEGER NOT NULL",
    "game_version":               "INTEGER NOT NULL DEFAULT 0",
    "gitadora_id":                "INTEGER DEFAULT 0",
    "name":                       "TEXT DEFAULT 'kors k'",
    "title":                      "TEXT DEFAULT 'MONKEY BUSINESS'",
    "charaid":                    "INTEGER DEFAULT 0",
    "stickers": "JSON_LIST",
    "rival_card_ids": "JSON_LIST",
    # Drummania sub-object
    "dm_customdata_playstyle": "JSON_LIST",
    "dm_customdata_custom": "JSON_LIST",
    "dm_skilldata_skill":         "INTEGER DEFAULT 0",
    "dm_skilldata_allskill":      "INTEGER DEFAULT 0",
    "dm_record_max_skill":        "INTEGER DEFAULT 0",
    "dm_record_max_all_skill":    "INTEGER DEFAULT 0",
    "dm_record_max_clear_diff":   "INTEGER DEFAULT 0",
    "dm_record_max_full_diff":    "INTEGER DEFAULT 0",
    "dm_record_max_exce_diff":    "INTEGER DEFAULT 0",
    "dm_playinfo_play":           "INTEGER DEFAULT 0",
    "dm_playinfo_playtime":       "INTEGER DEFAULT 0",
    "dm_playinfo_session_cnt":    "INTEGER DEFAULT 0",
    "dm_playinfo_saved_cnt":      "INTEGER DEFAULT 0",
    "dm_playinfo_extra_stage":    "INTEGER DEFAULT 0",
    "dm_playinfo_extra_play":     "INTEGER DEFAULT 0",
    "dm_playinfo_extra_clear":    "INTEGER DEFAULT 0",
    "dm_playinfo_encore_play":    "INTEGER DEFAULT 0",
    "dm_playinfo_encore_clear":   "INTEGER DEFAULT 0",
    "dm_playinfo_pencore_play":   "INTEGER DEFAULT 0",
    "dm_playinfo_pencore_clear":  "INTEGER DEFAULT 0",
    "dm_playinfo_clear_num":      "INTEGER DEFAULT 0",
    "dm_playinfo_full_num":       "INTEGER DEFAULT 0",
    "dm_playinfo_exce_num":       "INTEGER DEFAULT 0",
    "dm_playinfo_no_num":         "INTEGER DEFAULT 0",
    "dm_playinfo_e_num":          "INTEGER DEFAULT 0",
    "dm_playinfo_d_num":          "INTEGER DEFAULT 0",
    "dm_playinfo_c_num":          "INTEGER DEFAULT 0",
    "dm_playinfo_b_num":          "INTEGER DEFAULT 0",
    "dm_playinfo_a_num":          "INTEGER DEFAULT 0",
    "dm_playinfo_s_num":          "INTEGER DEFAULT 0",
    "dm_playinfo_ss_num":         "INTEGER DEFAULT 0",
    "dm_playinfo_last_category":  "INTEGER DEFAULT 0",
    "dm_playinfo_last_musicid":   "INTEGER DEFAULT 0",
    "dm_playinfo_last_seq":       "INTEGER DEFAULT 0",
    "dm_playinfo_disp_level":     "INTEGER DEFAULT 0",
    "dm_tutorial_progress":       "INTEGER DEFAULT 0",
    "dm_tutorial_disp_state":     "INTEGER DEFAULT 0",
    "dm_information": "JSON_LIST",
    "dm_reward": "JSON_LIST",
    "dm_favorite_music_list_1": "JSON_LIST",
    "dm_favorite_music_list_2": "JSON_LIST",
    "dm_favorite_music_list_3": "JSON_LIST",
    "dm_recommend_musicid_list": "JSON_LIST",
    "dm_thanks_medal_medal":      "INTEGER DEFAULT 0",
    "dm_thanks_medal_granted_total_medal":"INTEGER DEFAULT 0",
    "dm_record_diff": "JSON_LIST",
    "dm_record_clear": "JSON_LIST",
    "dm_groove_extra_gauge":      "INTEGER DEFAULT 0",
    "dm_groove_encore_gauge":     "INTEGER DEFAULT 0",
    "dm_groove_encore_cnt":       "INTEGER DEFAULT 0",
    "dm_groove_encore_success":   "INTEGER DEFAULT 0",
    "dm_groove_unlock_point":     "INTEGER DEFAULT 0",
    # Guitarfreaks sub-object (mirrors dm_ prefix -> gf_)
    "gf_customdata_playstyle": "JSON_LIST",
    "gf_customdata_custom": "JSON_LIST",
    "gf_skilldata_skill":         "INTEGER DEFAULT 0",
    "gf_skilldata_allskill":      "INTEGER DEFAULT 0",
    "gf_record_max_skill":        "INTEGER DEFAULT 0",
    "gf_record_max_all_skill":    "INTEGER DEFAULT 0",
    "gf_record_max_clear_diff":   "INTEGER DEFAULT 0",
    "gf_record_max_full_diff":    "INTEGER DEFAULT 0",
    "gf_record_max_exce_diff":    "INTEGER DEFAULT 0",
    "gf_playinfo_play":           "INTEGER DEFAULT 0",
    "gf_playinfo_playtime":       "INTEGER DEFAULT 0",
    "gf_playinfo_session_cnt":    "INTEGER DEFAULT 0",
    "gf_playinfo_saved_cnt":      "INTEGER DEFAULT 0",
    "gf_playinfo_extra_stage":    "INTEGER DEFAULT 0",
    "gf_playinfo_extra_play":     "INTEGER DEFAULT 0",
    "gf_playinfo_extra_clear":    "INTEGER DEFAULT 0",
    "gf_playinfo_encore_play":    "INTEGER DEFAULT 0",
    "gf_playinfo_encore_clear":   "INTEGER DEFAULT 0",
    "gf_playinfo_pencore_play":   "INTEGER DEFAULT 0",
    "gf_playinfo_pencore_clear":  "INTEGER DEFAULT 0",
    "gf_playinfo_clear_num":      "INTEGER DEFAULT 0",
    "gf_playinfo_full_num":       "INTEGER DEFAULT 0",
    "gf_playinfo_exce_num":       "INTEGER DEFAULT 0",
    "gf_playinfo_no_num":         "INTEGER DEFAULT 0",
    "gf_playinfo_e_num":          "INTEGER DEFAULT 0",
    "gf_playinfo_d_num":          "INTEGER DEFAULT 0",
    "gf_playinfo_c_num":          "INTEGER DEFAULT 0",
    "gf_playinfo_b_num":          "INTEGER DEFAULT 0",
    "gf_playinfo_a_num":          "INTEGER DEFAULT 0",
    "gf_playinfo_s_num":          "INTEGER DEFAULT 0",
    "gf_playinfo_ss_num":         "INTEGER DEFAULT 0",
    "gf_playinfo_last_category":  "INTEGER DEFAULT 0",
    "gf_playinfo_last_musicid":   "INTEGER DEFAULT 0",
    "gf_playinfo_last_seq":       "INTEGER DEFAULT 0",
    "gf_playinfo_disp_level":     "INTEGER DEFAULT 0",
    "gf_tutorial_progress":       "INTEGER DEFAULT 0",
    "gf_tutorial_disp_state":     "INTEGER DEFAULT 0",
    "gf_information": "JSON_LIST",
    "gf_reward": "JSON_LIST",
    "gf_favorite_music_list_1": "JSON_LIST",
    "gf_favorite_music_list_2": "JSON_LIST",
    "gf_favorite_music_list_3": "JSON_LIST",
    "gf_recommend_musicid_list": "JSON_LIST",
    "gf_thanks_medal_medal":      "INTEGER DEFAULT 0",
    "gf_thanks_medal_granted_total_medal":"INTEGER DEFAULT 0",
    "gf_record_diff": "JSON_LIST",
    "gf_record_clear": "JSON_LIST",
    "gf_groove_extra_gauge":      "INTEGER DEFAULT 0",
    "gf_groove_encore_gauge":     "INTEGER DEFAULT 0",
    "gf_groove_encore_cnt":       "INTEGER DEFAULT 0",
    "gf_groove_encore_success":   "INTEGER DEFAULT 0",
    "gf_groove_unlock_point":     "INTEGER DEFAULT 0",
    # Misc
    "params": "JSON_LIST",
}

# =============================================================================
# Gitadora scores — play log (used as f"{g}_scores" where g = drummania|guitarfreaks)
# =============================================================================

GITADORA_SCORES = {
    "doc_id":            "INTEGER PRIMARY KEY AUTOINCREMENT",
    "timestamp":         "REAL DEFAULT 0.0",
    "game_version":      "INTEGER DEFAULT 0",
    "gitadora_id":       "INTEGER DEFAULT 0",
    "data_version":      "INTEGER DEFAULT 0",
    "musicid":           "INTEGER DEFAULT 0",
    "seq":               "INTEGER DEFAULT 0",
    "skill":             "INTEGER DEFAULT 0",
    "new_skill":         "INTEGER DEFAULT 0",
    "clear":             "INTEGER DEFAULT 0",
    "auto_clear":        "INTEGER DEFAULT 0",
    "fullcombo":         "INTEGER DEFAULT 0",
    "excellent":         "INTEGER DEFAULT 0",
    "medal":             "INTEGER DEFAULT 0",
    "perc":              "INTEGER DEFAULT 0",
    "new_perc":          "INTEGER DEFAULT 0",
    "rank":              "INTEGER DEFAULT 0",
    "score":             "INTEGER DEFAULT 0",
    "combo":             "INTEGER DEFAULT 0",
    "max_combo_perc":    "INTEGER DEFAULT 0",
    "flags":             "INTEGER DEFAULT 0",
    "phrase_combo_perc": "INTEGER DEFAULT 0",
    "perfect":           "INTEGER DEFAULT 0",
    "great":             "INTEGER DEFAULT 0",
    "good":              "INTEGER DEFAULT 0",
    "ok":                "INTEGER DEFAULT 0",
    "miss":              "INTEGER DEFAULT 0",
    "perfect_perc":      "INTEGER DEFAULT 0",
    "great_perc":        "INTEGER DEFAULT 0",
    "good_perc":         "INTEGER DEFAULT 0",
    "ok_perc":           "INTEGER DEFAULT 0",
    "miss_perc":         "INTEGER DEFAULT 0",
    "meter":             "INTEGER DEFAULT 0",
    "meter_prog":        "INTEGER DEFAULT 0",
    "before_meter":      "INTEGER DEFAULT 0",
    "before_meter_prog": "INTEGER DEFAULT 0",
    "is_new_meter":      "INTEGER DEFAULT 0",
    "phrase_data_num":   "INTEGER DEFAULT 0",
    "phrase_addr": "JSON_LIST",
    "phrase_type": "JSON_LIST",
    "phrase_status": "JSON_LIST",
    "phrase_end_addr":   "INTEGER DEFAULT 0",
}

# =============================================================================
# Gitadora scores best
# =============================================================================

GITADORA_SCORES_BEST = {
    "doc_id":      "INTEGER PRIMARY KEY AUTOINCREMENT",
    "gitadora_id": "INTEGER DEFAULT 0",
    "musicid":     "INTEGER DEFAULT 0",
    "seq":         "INTEGER DEFAULT 0",
    "skill":       "INTEGER DEFAULT 0",
    "clear":       "INTEGER DEFAULT 0",
    "fullcombo":   "INTEGER DEFAULT 0",
    "excellent":   "INTEGER DEFAULT 0",
    "perc":        "INTEGER DEFAULT 0",
    "rank":        "INTEGER DEFAULT 0",
    "meter":       "INTEGER DEFAULT 0",
    "meter_prog":  "INTEGER DEFAULT 0",
}

# =============================================================================
# Shop
# =============================================================================

SHOP = {
    "doc_id": "INTEGER PRIMARY KEY AUTOINCREMENT",
    "pcbid":  "INTEGER DEFAULT 0",
    "opname": "INTEGER DEFAULT 0",
}

# =============================================================================
# Map table name -> schema for all tables
# =============================================================================

ALL_SCHEMAS = {
    # Profiles
    "iidx_profile":       IIDX_PROFILE,
    "ddr_profile":        DDR_PROFILE,
    "sdvx_profile":       SDVX_PROFILE,
    "gitadora_profile":   GITADORA_PROFILE,
    "nostalgia_profile":  NOSTALGIA_PROFILE,
    "dancerush_profile":  DRS_PROFILE,
    # IIDX
    "iidx_scores":        IIDX_SCORES,
    "iidx_scores_best":   IIDX_SCORES_BEST,
    "iidx_score_stats":   IIDX_SCORE_STATS,
    "iidx_class":         IIDX_CLASS,
    "iidx_class_best":    IIDX_CLASS_BEST,
    # DDR
    "ddr_scores":         DDR_SCORES,
    "ddr_scores_best":    DDR_SCORES_BEST,
    # SDVX
    "sdvx_scores":        SDVX_SCORES,
    "sdvx_scores_best":   SDVX_SCORES_BEST,
    # DRS
    "drs_scores":         DRS_SCORES,
    "drs_scores_best":    DRS_SCORES_BEST,
    # Nostalgia
    "nostalgia_scores":       NOSTALGIA_SCORES,
    "nostalgia_scores_best":  NOSTALGIA_SCORES_BEST,
    # Gitadora
    "drummania_scores":        GITADORA_SCORES,
    "drummania_scores_best":   GITADORA_SCORES_BEST,
    "guitarfreaks_scores":     GITADORA_SCORES,
    "guitarfreaks_scores_best":GITADORA_SCORES_BEST,
    # Shop
    "shop":                SHOP,
}


def get_schema(table_name):
    """Get the explicit-column schema for a table, or None if not defined."""
    return ALL_SCHEMAS.get(table_name, None)
