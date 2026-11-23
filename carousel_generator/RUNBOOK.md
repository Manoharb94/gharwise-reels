# Daily Gharwise Instagram carousel (runs 2:00 PM IST)

Account: Instagram "gharwiseapp", Windsor account id 17841455269283373 (connector `instagram`).

1. `git clone --depth 1 https://github.com/Manoharb94/gharwise-reels` and `git clone --depth 1 https://github.com/Manoharb94/gharwise-app` (needs repo access for both; push access for gharwise-reels).
2. Pick the first topic in `carousel_generator/topics.json` with `"status":"pending"`.
   If none are pending, write ONE new topic yourself (same JSON shape, new id t10, t11...), based on a real feature you verified in `gharwise-app/www/index.html`; screens available: home, home_family, plan, goals, fam, track, list, rep, rep_next, fixed. Never invent features, numbers or claims.
3. `pip install playwright pillow` if needed (`--break-system-packages`), then
   `python3 carousel_generator/shoot_screens.py <gharwise-app>/www /tmp/scr`
   `python3 carousel_generator/build_post.py <topic_id> /tmp/scr gharwise-reels/carousel_<id>_<slug>`
   Look at the slides (contact sheet). Fix overflowing text before posting.
4. Commit and push the new folder to `main` (never delete anything in the repo). Verify each raw URL returns 200:
   `https://raw.githubusercontent.com/Manoharb94/gharwise-reels/main/carousel_<id>_<slug>/<slug>_slide<N>.jpg`
5. Check the account has not already posted today (Windsor `get_data`, instagram) to avoid duplicates.
6. Windsor `execute_action` connector `instagram`, action `create_carousel_post`, account above, `image_urls` in order, `caption` from the topic.
7. Set the topic `"status":"posted"` plus `"posted_at"` and `"media_id"` in topics.json, commit and push.
8. Tell the user which topic went live. Music cannot be added through the API.
