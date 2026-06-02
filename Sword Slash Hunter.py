import cv2
import numpy as np
import random
import platform
from PIL import ImageFont, ImageDraw, Image

# ==========================================
# PENGATURAN UTAMA 
# ==========================================
WIDTH, HEIGHT = 640, 480
NAMA_FILE_FONT = "aAsianNinja.ttf" 

# Ukuran Elemen
title_w, title_h = 350, 140
btn_w, btn_h = 180, 30
sword_w, sword_h = 40, 150
heart_size = 30
enemy_radius = 25
enemy_size = enemy_radius * 2
enemy_anim_frame = 0
enemy_anim_counter = 0

BORDER_PADDING = 10

# --- AUDIO ---
if platform.system() == "Windows":
    import winsound
    audio_enabled = True
else:
    audio_enabled = False

def play_bgm():
    if audio_enabled:
        winsound.PlaySound("backsound.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

def play_gameover_bgm():
    if audio_enabled:
        winsound.PlaySound("gameover_bgm.wav", winsound.SND_ASYNC | winsound.SND_LOOP)

def stop_audio():
    if audio_enabled:
        winsound.PlaySound(None, winsound.SND_PURGE)

# --- LOAD GAMBAR ---
img_title = cv2.resize(cv2.imread('title_banner.png', cv2.IMREAD_UNCHANGED), (title_w, title_h))
img_btn1 = cv2.resize(cv2.imread('btn_lvl1.png', cv2.IMREAD_UNCHANGED), (btn_w, btn_h))
img_btn2 = cv2.resize(cv2.imread('btn_lvl2.png', cv2.IMREAD_UNCHANGED), (btn_w, btn_h))
img_btn3 = cv2.resize(cv2.imread('btn_lvl3.png', cv2.IMREAD_UNCHANGED), (btn_w, btn_h))
img_btn_exit = cv2.resize(cv2.imread('btn_exit.png', cv2.IMREAD_UNCHANGED), (btn_w, btn_h))

img_playing_bg = cv2.resize(cv2.imread('playing_bg.jpg'), (WIDTH, HEIGHT))
img_gameover = cv2.resize(cv2.imread('gameover_bg.jpg'), (WIDTH, HEIGHT))

img_sword = cv2.resize(cv2.imread('sword.png', cv2.IMREAD_UNCHANGED), (sword_w, sword_h))
img_heart = cv2.resize(cv2.imread('heart.png', cv2.IMREAD_UNCHANGED), (heart_size, heart_size))

# --- LOAD ENEMY SPRITE ---
enemy_frames = []
sheet = cv2.imread('enemy.png', cv2.IMREAD_UNCHANGED)
frame_width = sheet.shape[1] // 4
frame_height = sheet.shape[0]

for i in range(4):
    frame = sheet[0:frame_height, i * frame_width:(i + 1) * frame_width]
    frame = cv2.resize(frame, (enemy_size, enemy_size))
    enemy_frames.append(frame)

img_score_bg = cv2.imread('score_bg.png', cv2.IMREAD_UNCHANGED)
img_health_bg = cv2.imread('health_bg.png', cv2.IMREAD_UNCHANGED)

# --- LOAD VIDEO ---
menu_cap = cv2.VideoCapture('menu_vid.mp4')
gameover_cap = cv2.VideoCapture('gameover_vid.mp4')

# ==========================================
# FUNCTION 
# ==========================================

def draw_custom_text(img, text, font_path, font_size, color_bgr, pos_x=0, pos_y=0, center_x=False, center_y=False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    if center_x: pos_x = (img.shape[1] - text_w) // 2
    if center_y: pos_y = (img.shape[0] - text_h) // 2
    b, g, r = color_bgr
    draw.text((pos_x, pos_y), text, font=font, fill=(r, g, b))
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def draw_fading_text(img, text, font_path, font_size, color_bgr, alpha, center_x=False, pos_y=0):
    overlay = img.copy()
    img_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_img)
    
    font = ImageFont.truetype(font_path, font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    pos_x = (img.shape[1] - text_w) // 2 if center_x else 0
    draw.text((pos_x, pos_y), text, font=font, fill=color_bgr)
    
    result = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return cv2.addWeighted(result, alpha, img, 1 - alpha, 0)

def apply_morphology(mask_img):
    kernel = np.ones((7, 7), np.uint8)
    cleaned = cv2.erode(mask_img, kernel, iterations=1)
    cleaned = cv2.dilate(cleaned, kernel, iterations=2)
    return cleaned

def draw_dashed_line(img, y_pos):
    dist = 20 
    for i in range(0, img.shape[1], dist*2): 
        cv2.line(img, (i, y_pos), (i + dist, y_pos), (255, 255, 255), 1)

def overlay_transparent(bg_img, fg_img, x, y):
    h, w = bg_img.shape[:2]
    fh, fw = fg_img.shape[:2]
    if x >= w or y >= h or x + fw <= 0 or y + fh <= 0: return bg_img
    x1, x2 = max(0, x), min(w, x + fw)
    y1, y2 = max(0, y), min(h, y + fh)
    fg_x1, fg_x2 = max(0, -x), min(fw, w - x)
    fg_y1, fg_y2 = max(0, -y), min(fh, h - y)
    crop_fg = fg_img[fg_y1:fg_y2, fg_x1:fg_x2]
    crop_bg = bg_img[y1:y2, x1:x2]
    if crop_fg.shape[2] == 4:
        alpha = crop_fg[:, :, 3] / 255.0
        alpha = np.expand_dims(alpha, axis=2)
        bg_img[y1:y2, x1:x2] = ((1.0 - alpha) * crop_bg + alpha * crop_fg[:, :, :3]).astype(np.uint8)
    else:
        bg_img[y1:y2, x1:x2] = crop_fg[:, :, :3]
    return bg_img

# ==========================================
# VARIABEL GAME STATE
# ==========================================
score = 0
health = 3
garis_batas = int(HEIGHT * 0.6) 
game_state = "MENU"
current_speed = 8
enemy = [random.randint(100, WIDTH-100), 0, current_speed]
prev_tip = None
running = True
is_slashing = False
slash_timer = 0

# --- POSISI TOMBOL MENU ---
start_x = (WIDTH - btn_w) // 2
start_y = 220 
gap = 15 
btn_lvl1_pos = (start_x, start_y, start_x + btn_w, start_y + btn_h)
btn_lvl2_pos = (start_x, start_y + btn_h + gap, start_x + btn_w, start_y + (btn_h * 2) + gap)
btn_lvl3_pos = (start_x, start_y + (btn_h * 2) + (gap * 2), start_x + btn_w, start_y + (btn_h * 3) + (gap * 2))
btn_exit_pos = (start_x, start_y + (btn_h * 3) + (gap * 3), start_x + btn_w, start_y + (btn_h * 4) + (gap * 3))

def start_game():
    global game_state, score, health, enemy, current_speed, prev_tip
    score = 0
    health = 3
    enemy = [random.randint(100, WIDTH-100), 0, current_speed]
    prev_tip = None
    cv2.namedWindow("Game PCV")
    cv2.moveWindow("Game PCV", 40, 50) 
    debug_w, debug_h = WIDTH // 2, HEIGHT // 2
    pos_x_debug = 40 + WIDTH + 30
    cv2.namedWindow("Bareface (Kamera)", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Bareface (Kamera)", debug_w, debug_h)
    cv2.moveWindow("Bareface (Kamera)", pos_x_debug, 50) 
    cv2.namedWindow("Skin Detection Debug", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Skin Detection Debug", debug_w, debug_h)
    cv2.moveWindow("Skin Detection Debug", pos_x_debug, 50 + debug_h + 40) 
    game_state = "PLAYING"

def mouse_click_handler(event, x, y, flags, param):
    global game_state, current_speed, running
    if event == cv2.EVENT_LBUTTONDOWN:
        if game_state == "MENU":
            if btn_lvl1_pos[0] <= x <= btn_lvl1_pos[2] and btn_lvl1_pos[1] <= y <= btn_lvl1_pos[3]:
                current_speed = 7
                start_game()
            elif btn_lvl2_pos[0] <= x <= btn_lvl2_pos[2] and btn_lvl2_pos[1] <= y <= btn_lvl2_pos[3]:
                current_speed = 14
                start_game()
            elif btn_lvl3_pos[0] <= x <= btn_lvl3_pos[2] and btn_lvl3_pos[1] <= y <= btn_lvl3_pos[3]:
                current_speed = 22
                start_game()
            elif btn_exit_pos[0] <= x <= btn_exit_pos[2] and btn_exit_pos[1] <= y <= btn_exit_pos[3]:
                running = False 
        elif game_state == "GAMEOVER":
            game_state = "MENU"
            cv2.namedWindow("Game PCV")
            cv2.moveWindow("Game PCV", 40, 50) 
            menu_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            play_bgm() # Putar kembali BGM utama saat kembali ke menu

cv2.namedWindow("Game PCV")
cv2.moveWindow("Game PCV", 40, 50) 
cv2.setMouseCallback("Game PCV", mouse_click_handler)
cap = cv2.VideoCapture(0)
play_bgm()

# ==========================================
# LOOP UTAMA
# ==========================================
popup_timer = 0
last_hit_text = ""
while running:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    key = cv2.waitKey(1) & 0xFF
    
    if game_state == "MENU":
        m_ret, m_frame = menu_cap.read()
        if not m_ret:
            menu_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _, m_frame = menu_cap.read()
        menu_frame = cv2.resize(m_frame, (WIDTH, HEIGHT))
        title_x = (WIDTH - title_w) // 2
        title_y = 60
        menu_frame = overlay_transparent(menu_frame, img_title, title_x, title_y)
        menu_frame = overlay_transparent(menu_frame, img_btn1, btn_lvl1_pos[0], btn_lvl1_pos[1])
        menu_frame = overlay_transparent(menu_frame, img_btn2, btn_lvl2_pos[0], btn_lvl2_pos[1])
        menu_frame = overlay_transparent(menu_frame, img_btn3, btn_lvl3_pos[0], btn_lvl3_pos[1])
        menu_frame = overlay_transparent(menu_frame, img_btn_exit, btn_exit_pos[0], btn_exit_pos[1])
        cv2.imshow("Game PCV", menu_frame)
        if key == ord('q'): running = False

    elif game_state == "PLAYING":
        focus_frame = frame
        cv2.line(focus_frame, (0, garis_batas), (WIDTH, garis_batas), (0, 0, 255), 2)
        cv2.imshow("Bareface (Kamera)", focus_frame)
        display_f = img_playing_bg.copy()
        blurred = cv2.GaussianBlur(focus_frame, (11, 11), 0)
        hsv = cv2.cvtColor(focus_frame, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([100, 100, 50], dtype=np.uint8) 
        upper_skin = np.array([140, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        
        def apply_morphology_improved(mask_img):
            kernel = np.ones((7, 7), np.uint8)
            cleaned = cv2.erode(mask_img, kernel, iterations=1)
            cleaned = cv2.dilate(cleaned, kernel, iterations=3) 
            return cleaned
            
        mask_cleaned = apply_morphology_improved(mask)
        mask_below_line = mask_cleaned.copy()
        mask_below_line[0:garis_batas, :] = 0
        cv2.imshow("Skin Detection Debug", mask_below_line)
        draw_dashed_line(display_f, garis_batas)
        contours, _ = cv2.findContours(mask_below_line, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        palm_center = None
        sword_rect = None
        current_tip = None
        
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            if cv2.contourArea(cnt) > 3000:
                single_mask = np.zeros_like(mask_below_line)
                cv2.drawContours(single_mask, [cnt], -1, 255, -1)
                dist_transform = cv2.distanceTransform(single_mask, cv2.DIST_L2, 5)
                _, max_val, _, max_loc = cv2.minMaxLoc(dist_transform)
                if max_val > 10:
                    cx, cy = max_loc
                    palm_center = (cx, cy)
                    offset_up = 20
                    p1 = (cx - sword_w//2, cy - sword_h - offset_up)
                    p2 = (cx + sword_w//2, cy - offset_up)
                    sword_rect = (p1, p2)
                    current_tip = (cx, cy - sword_h - offset_up)
                    if prev_tip is not None: 
                        dx = current_tip[0] - prev_tip[0]
                        dy = current_tip[1] - prev_tip[1]
                        distance = np.sqrt(dx**2 + dy**2)
                        if distance > 60:
                            is_slashing = True
                            slash_timer = 8
                        if distance > 35:
                            cv2.line(display_f, prev_tip, current_tip, (255,255,0), 14, cv2.LINE_AA)
                            cv2.line(display_f, prev_tip, current_tip, (255,255,255), 4, cv2.LINE_AA) 
                    prev_tip = current_tip
                    display_f = overlay_transparent(display_f, img_sword, p1[0], p1[1])
            else:
                prev_tip = None
        else:
            prev_tip = None

        enemy[1] += enemy[2]
        ex, ey = enemy[0], enemy[1]
        enemy_anim_counter += 1
        if enemy_anim_counter >= 5:
            enemy_anim_counter = 0
            enemy_anim_frame = (enemy_anim_frame + 1) % len(enemy_frames)
        display_f = overlay_transparent(display_f, enemy_frames[enemy_anim_frame], ex - enemy_radius, ey - enemy_radius)
        
        if palm_center and sword_rect:
            s_p1, s_p2 = sword_rect
            normal_hit = (s_p1[0] < ex < s_p2[0] and s_p1[1] < ey < s_p2[1])
            slash_hit = (is_slashing and prev_tip is not None and abs(ex - current_tip[0]) < 80 and abs(ey - current_tip[1]) < 80)

            if slash_hit:
                score += 3
                popup_timer = 15
                last_hit_text = "+3 SLASH!"
                enemy = [random.randint(100, WIDTH-100), 0, current_speed + random.randint(-1,2)]
            elif normal_hit:
                score += 1
                popup_timer = 15
                last_hit_text = "+1 HIT!"
                enemy = [random.randint(100, WIDTH-100), 0, current_speed + random.randint(-1,2)]
        
        if enemy[1] > HEIGHT:
            health -= 1
            if health <= 0:
                game_state = "GAMEOVER"
                play_gameover_bgm() # Mainkan BGM Game Over
                try:
                    cv2.destroyWindow("Skin Detection Debug")
                    cv2.destroyWindow("Bareface (Kamera)")
                except: pass
            else:
                enemy = [random.randint(100, WIDTH-100), 0, current_speed]

        if slash_timer > 0:
            alpha = slash_timer / 8.0
            display_f = draw_fading_text(display_f, "SLASH!", NAMA_FILE_FONT, 120, (255, 255, 0), alpha, center_x=True, pos_y=180)
            display_f = draw_fading_text(display_f, "SLASH!", NAMA_FILE_FONT, 115, (255, 255, 255), alpha, center_x=True, pos_y=182)
            slash_timer -= 1
            
        if popup_timer > 0:
            pos_y_notif = 120 - (15 - popup_timer) * 2
            display_f = draw_fading_text(display_f, last_hit_text, NAMA_FILE_FONT, 50, (100, 255, 255), popup_timer/15.0, center_x=True, pos_y=pos_y_notif)
            popup_timer -= 1
        else:
            is_slashing = False

        score_x, score_y = 20, 15
        score_w, score_h = 160, 35 
        bg_s_x, bg_s_y = score_x - BORDER_PADDING, score_y - BORDER_PADDING
        bg_s_w, bg_s_h = score_w + (BORDER_PADDING * 2), score_h + (BORDER_PADDING * 2)
        resized_s_bg = cv2.resize(img_score_bg, (bg_s_w, bg_s_h))
        display_f = overlay_transparent(display_f, resized_s_bg, bg_s_x, bg_s_y)
        display_f = draw_custom_text(display_f, f"SCORE: {score}", NAMA_FILE_FONT, 30, (255, 255, 255), pos_x=score_x+10, pos_y=score_y+3)

        box_w = (heart_size * 3) + (35 * 2) + (BORDER_PADDING * 2)
        box_h = heart_size + (BORDER_PADDING * 2)
        box_left = (WIDTH - 40) - 70 - BORDER_PADDING
        box_top = 20 - BORDER_PADDING
        resized_h_bg = cv2.resize(img_health_bg, (box_w, box_h))
        display_f = overlay_transparent(display_f, resized_h_bg, box_left, box_top)

        for i in range(3):
            x_heart = (WIDTH - 37) - (i * 30)
            y_heart = 20
            if i < health:
                display_f = overlay_transparent(display_f, img_heart, x_heart, y_heart)
            else:
                cv2.rectangle(display_f, (x_heart, y_heart), (x_heart+25, y_heart+25), (100, 100, 100), -1)

        cv2.imshow("Game PCV", display_f)
        if key == ord('m'):
            game_state = "MENU"
            play_bgm()
            cv2.namedWindow("Game PCV")
            cv2.moveWindow("Game PCV", 40, 50) 
            try:
                cv2.destroyWindow("Skin Detection Debug")
                cv2.destroyWindow("Bareface (Kamera)")
            except: pass
        elif key == ord('q'): running = False

    elif game_state == "GAMEOVER":
        go_ret, go_frame = gameover_cap.read()
        if not go_ret:
            gameover_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            _, go_frame = gameover_cap.read()
        go_frame = cv2.resize(go_frame, (WIDTH, HEIGHT))
        go_frame = draw_custom_text(go_frame, "GAME OVER", NAMA_FILE_FONT, 80, (255, 255, 255), center_x=True, pos_y=HEIGHT//2 - 95)
        go_frame = draw_custom_text(go_frame, f"SKOR AKHIR: {score}", NAMA_FILE_FONT, 30, (100, 255, 255), center_x=True, pos_y=HEIGHT//2 -15)
        go_frame = draw_custom_text(go_frame, "- KLIK UNTUK KEMBALI KE MENU -", NAMA_FILE_FONT, 25, (200, 200, 200), center_x=True, pos_y=HEIGHT//2 + 40)
        
        cv2.imshow("Game PCV", go_frame)
        if key == ord('q'): running = False

stop_audio()
menu_cap.release() 
gameover_cap.release()
cap.release()
cv2.destroyAllWindows()
