// Homepage artwork: Kitsune (the guardian), the dragon (the struggle), Pegasus (freedom).
// Inside a scene, that scene's loop plays by itself (rain, lanterns, the dragon coiling, wings
// beating), so the page is alive even when you stop scrolling. Between scenes, the journey film
// follows the scroll: down plays it forward, up rewinds it. The journeys start and end on exactly
// the frames the loops start on, so the hand-offs are seamless.
(function () {
    'use strict';

    const section = document.querySelector('.myth');
    if (!section) return;
    const stage = section.querySelector('.myth-stage');
    const film = section.querySelector('.myth-film');
    const loops = [...section.querySelectorAll('.myth-loop')];   // kitsune, dragon, pegasus
    const chapters = [...section.querySelectorAll('.chapter')];
    const texts = chapters.map(c => c.querySelector('.chapter-text')).filter(Boolean);
    const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const small = window.matchMedia('(max-width: 820px)').matches;

    // Journeys in story time (see storyTime; each has its own tall empty section, so they take
    // their time) and in film time: up the torii tunnel into the ink mountains, then west along the
    // Silk Road (ink dunes, the painted Greek coast, the dragon climbing into the clouds, through the
    // cloud) to Pegasus. `film` pins
    // scroll progress to film seconds, one key per painted checkpoint.
    const JOURNEYS = [
        { at: [1.85, 3.1], film: [[0, 0], [1, 10.1]] },
        { at: [3.85, 5.1], film: [[0, 10.1], [0.28, 15.2], [0.54, 20.33], [0.84, 25.45], [1, 27.8]] },
    ];
    const TONES = ['dark', 'light', 'dark'];

    const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

    // T runs 0..7: the section (chapter or journey) that crosses the middle of the screen, plus how far through it.
    function storyTime() {
        const mid = window.innerHeight / 2;
        for (let i = chapters.length - 1; i >= 0; i--) {
            const r = chapters[i].getBoundingClientRect();
            if (r.top <= mid) return i + clamp((mid - r.top) / r.height, 0, 1);
        }
        return 0;
    }

    // Which scene the scroll is in (-1 while on a journey) and where the film should be.
    function locate(T) {
        let scene = 0, time = 0;
        for (const [i, j] of JOURNEYS.entries()) {
            const [a, b] = j.at;
            if (T < a) return { scene, time };
            if (T < b) return { scene: -1, time: along(j.film, (T - a) / (b - a)) };
            scene = i + 1;
            time = j.film[j.film.length - 1][1];
        }
        return { scene, time };
    }

    function along(keys, p) {
        for (let i = 1; i < keys.length; i++) {
            const [p0, t0] = keys[i - 1], [p1, t1] = keys[i];
            if (p <= p1) return t0 + (t1 - t0) * (p - p0) / (p1 - p0);
        }
        return keys[keys.length - 1][1];
    }

    [film, ...loops].forEach(v => { v.src = small ? v.dataset.srcSmall : v.dataset.src; });

    let current = 0, shown = 0;
    function enter(scene) {
        if (scene === current) return;
        current = scene;
        loops.forEach((v, i) => {
            const on = i === scene;
            v.classList.toggle('is-on', on);
            if (still) return;
            if (on) {
                v.currentTime = 0;                   // the loop starts on the frame the journey ended on
                v.play().catch(() => {});            // blocked autoplay leaves the sharp poster
            } else {
                v.pause();
            }
        });
        if (scene >= 0) stage.dataset.tone = TONES[scene];
    }

    function frame() {
        const T = storyTime();
        const { scene, time } = locate(T);
        enter(scene);
        if (scene < 0) stage.dataset.tone = time < 5 ? 'dark' : time < 17.5 ? 'light' : 'dark';

        // load what comes next a little ahead of time
        JOURNEYS.forEach((j, i) => {
            if (T > j.at[0] - 0.7 && loops[i + 1].preload !== 'auto') loops[i + 1].preload = 'auto';
        });

        // ease the film toward the scroll position, never queueing a seek while one runs
        if (!still && film.readyState >= 1) {
            shown += (time - shown) * 0.2;
            if (Math.abs(time - shown) < 0.02) shown = time;
            if (!film.seeking && Math.abs(film.currentTime - shown) > 1 / 48) film.currentTime = shown;
        }

        const moving = !still && JOURNEYS.some(({ at: [a, b] }) => T > a + 0.04 && T < b - 0.04);
        texts.forEach(el => el.classList.toggle('is-hidden', moving));
        if (!still) requestAnimationFrame(frame);
    }

    if (still) {
        // no motion: the sharp painting of whichever scene you are reading
        film.style.visibility = 'hidden';
        const update = () => {
            const T = storyTime();
            enter(T < 2.5 ? 0 : T < 4.5 ? 1 : 2);
            frame();
        };
        window.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
        current = -2;
        update();
    } else {
        current = -2;
        requestAnimationFrame(frame);
    }
})();
