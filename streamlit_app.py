color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin: 5px;
            transition: all 0.3s ease;
            min-width: 100px;
        }}
        
        .overlay-button:hover {{
            background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .overlay-button-secondary {{
            background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
        }}
        
        .overlay-button-secondary:hover {{
            background: linear-gradient(135deg, #5a6268 0%, #495057 100%);
        }}
        
        /* ゲーム完了時のスペシャルスタイル */
        .game-complete {{
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        }}
        
        .game-complete .stage-clear-title {{
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .game-complete .stage-clear-subtitle {{
            color: #fff;
        }}
        
        /* スマホ専用の調整 */
        @media (max-width: 480px) {{
            .stage-clear-content {{
                padding: 30px 20px;
                max-width: 280px;
            }}
            
            .stage-clear-title {{
                font-size: 24px;
            }}
            
            .stage-clear-subtitle {{
                font-size: 16px;
                margin-bottom: 25px;
            }}
            
            .overlay-button {{
                padding: 10px 20px;
                font-size: 14px;
                margin: 3px;
            }}
        }}
        </style>
    </head>
    <body>
        <div id="selected-word"></div>
        <div id="target-words">{target_display}</div>
        <div id="success-message" class="success-message">正解！</div>
        <div id="complete-message" class="complete-message">ステージクリア！</div>
        <div id="hint-popup" class="hint-popup">
            <div class="hint-word" id="hint-word"></div>
            <div id="hint-meaning"></div>
        </div>

        <!-- ステージクリアオーバーレイ -->
        <div id="stage-clear-overlay" class="stage-clear-overlay">
            <div class="stage-clear-content" id="stage-clear-content">
                <div class="stage-clear-title" id="overlay-title">ステージクリア！</div>
                <div class="stage-clear-subtitle" id="overlay-subtitle">おめでとうございます！</div>
                <div id="overlay-buttons">
                    <button class="overlay-button" id="next-stage-btn">次のステージへ</button>
                    <button class="overlay-button overlay-button-secondary" id="back-title-btn">タイトルへ戻る</button>
                </div>
            </div>
        </div>

        <div class="circle-container" id="circle-container">
            <canvas id="lineCanvas" width="260" height="260"></canvas>
            {button_html}
        </div>

        <script>
        // ページ読み込み時に即座にトップにスクロール
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                window.scrollTo(0, 0);
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
            }}, 50);
        }});

        // DOMContentLoaded時にもスクロール
        document.addEventListener('DOMContentLoaded', function() {{
            window.scrollTo(0, 0);
            document.body.scrollTop = 0;
            document.documentElement.scrollTop = 0;
        }});

        let isDragging = false;
        let selectedLetters = [];
        let selectedButtons = [];
        let points = [];
        let targetWords = {json.dumps(st.session_state.target_words)};
        let foundWords = {json.dumps(st.session_state.found_words)};
        let wordHints = {json.dumps(current_stage_info['hints'])};
        let currentStage = {st.session_state.current_stage};
        let totalStages = {len(STAGES)};

        const selectedWordDiv = document.getElementById('selected-word');
        const targetWordsDiv = document.getElementById('target-words');
        const successMessageDiv = document.getElementById('success-message');
        const completeMessageDiv = document.getElementById('complete-message');
        const hintPopupDiv = document.getElementById('hint-popup');
        const hintWordDiv = document.getElementById('hint-word');
        const hintMeaningDiv = document.getElementById('hint-meaning');
        const container = document.getElementById('circle-container');
        const canvas = document.getElementById('lineCanvas');
        const ctx = canvas.getContext('2d');

        // オーバーレイ要素
        const overlayDiv = document.getElementById('stage-clear-overlay');
        const overlayContentDiv = document.getElementById('stage-clear-content');
        const overlayTitleDiv = document.getElementById('overlay-title');
        const overlaySubtitleDiv = document.getElementById('overlay-subtitle');
        const nextStageBtn = document.getElementById('next-stage-btn');
        const backTitleBtn = document.getElementById('back-title-btn');

        function createAudioContext() {{
            try {{
                return new (window.AudioContext || window.webkitAudioContext)();
            }} catch (e) {{
                console.log('Web Audio API not supported');
                return null;
            }}
        }}

        const audioCtx = createAudioContext();

        function playSelectSound() {{
            if (!audioCtx) return;
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.1);
        }}

        function playCorrectSound() {{
            if (!audioCtx) return;
            const frequencies = [523, 659, 784, 1047];
            frequencies.forEach((freq, index) => {{
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.frequency.value = freq;
                oscillator.type = 'sine';
                const startTime = audioCtx.currentTime + index * 0.1;
                gainNode.gain.setValueAtTime(0.2, startTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.3);
                oscillator.start(startTime);
                oscillator.stop(startTime + 0.3);
            }});
        }}

        function playCompleteSound() {{
            if (!audioCtx) return;
            const melody = [523, 659, 784, 1047, 1319];
            melody.forEach((freq, index) => {{
                const oscillator = audioCtx.createOscillator();
                const gainNode = audioCtx.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscillator.frequency.value = freq;
                oscillator.type = 'triangle';
                const startTime = audioCtx.currentTime + index * 0.15;
                gainNode.gain.setValueAtTime(0.3, startTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, startTime + 0.4);
                oscillator.start(startTime);
                oscillator.stop(startTime + 0.4);
            }});
        }}

        function playWrongSound() {{
            if (!audioCtx) return;
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            oscillator.frequency.value = 200;
            oscillator.type = 'sawtooth';
            gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.3);
        }}

        function playHintSound() {{
            if (!audioCtx) return;
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            oscillator.frequency.value = 1000;
            oscillator.type = 'sine';
            gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
            oscillator.start(audioCtx.currentTime);
            oscillator.stop(audioCtx.currentTime + 0.2);
        }}

        function updateSelectedWord() {{
            selectedWordDiv.textContent = selectedLetters.join('');
        }}

        function updateTargetWordsDisplay() {{
            let targetBoxesHtml = [];
            let sortedWords = targetWords.slice().sort((a, b) => {{
                if (a.length !== b.length) {{
                    return a.length - b.length;
                }}
                return a.localeCompare(b);
            }});
            
            for (let word of sortedWords) {{
                let isFound = foundWords.includes(word);
                let boxesHtml = "";
                for (let i = 0; i < word.length; i++) {{
                    let letter = word[i];
                    if (isFound) {{
                        boxesHtml += '<span style="display: inline-block; width: 22px; height: 22px; border: 1px solid #333; background: white; color: #333; text-align: center; line-height: 22px; margin: 1px; font-size: 12px; font-weight: bold; border-radius: 3px; vertical-align: top;">' + letter + '</span>';
                    }} else {{
                        boxesHtml += '<span style="display: inline-block; width: 22px; height: 22px; border: 1px solid #ddd; background: white; text-align: center; line-height: 22px; margin: 1px; border-radius: 3px; vertical-align: top;"></span>';
                    }}
                }}
                targetBoxesHtml.push('<div class="word-hint-target" data-word="' + word + '" style="display: inline-block; margin: 4px; vertical-align: top; cursor: pointer; transition: transform 0.2s ease;">' + boxesHtml + '</div>');
            }}
            
            targetWordsDiv.innerHTML = targetBoxesHtml.join('');
            
            // ヒント機能のイベントリスナーを追加
            document.querySelectorAll('.word-hint-target').forEach(element => {{
                element.addEventListener('click', function(e) {{
                    e.preventDefault();
                    e.stopPropagation();
                    if (!isDragging) {{
                        showHint(this.dataset.word);
                    }}
                }});
                element.addEventListener('touchend', function(e) {{
                    e.preventDefault();
                    e.stopPropagation();
                    if (!isDragging) {{
                        showHint(this.dataset.word);
                    }}
                }});
            }});
        }}

        function showHint(word) {{
            if (wordHints[word]) {{
                // 英単語は表示せず、意味のみを表示
                hintWordDiv.textContent = "";
                hintMeaningDiv.textContent = wordHints[word];
                hintPopupDiv.classList.add('show');
                playHintSound();
                
                // 3秒後に自動的に隠す
                setTimeout(() => {{
                    hideHint();
                }}, 3000);
            }}
        }}

        function hideHint() {{
            hintPopupDiv.classList.remove('show');
        }}

        function showStageCompleteOverlay() {{
            if (currentStage >= totalStages) {{
                // 全ステージクリア
                overlayContentDiv.classList.add('game-complete');
                overlayTitleDiv.textContent = '全ステージクリア！';
                overlaySubtitleDiv.textContent = 'おめでとうございます！';
                nextStageBtn.style.display = 'none';
                backTitleBtn.textContent = 'タイトルへ戻る';
            }} else {{
                // 通常のステージクリア
                overlayContentDiv.classList.remove('game-complete');
                overlayTitleDiv.textContent = 'ステージクリア！';
                overlaySubtitleDiv.textContent = 'おめでとうございます！';
                nextStageBtn.style.display = 'inline-block';
                nextStageBtn.textContent = '次のステージへ';
                backTitleBtn.textContent = 'タイトルへ戻る';
            }}
            
            overlayDiv.classList.add('show');
        }}

        function hideStageCompleteOverlay() {{
            overlayDiv.classList.remove('show');
        }}

        function checkCorrectWord() {{
            const currentWord = selectedLetters.join('');
            if (currentWord && targetWords.includes(currentWord) && !foundWords.includes(currentWord)) {{
                foundWords.push(currentWord);
                updateTargetWordsDisplay();
                showSuccessMessage();
                playCorrectSound();
                
                if (foundWords.length === targetWords.length) {{
                    setTimeout(() => {{
                        showCompleteMessage();
                        playCompleteSound();
                        // オーバーレイを表示
                        setTimeout(() => {{
                            showStageCompleteOverlay();
                        }}, 1500);
                    }}, 1000);
                }}
                return true;
            }} else if (currentWord && currentWord.length >= 3) {{
                playWrongSound();
            }}
            return false;
        }}

        function showSuccessMessage() {{
            successMessageDiv.classList.add('show');
            setTimeout(() => {{
                successMessageDiv.classList.remove('show');
            }}, 1500);
        }}

        function showCompleteMessage() {{
            completeMessageDiv.classList.add('show');
            setTimeout(() => {{
                completeMessageDiv.classList.remove('show');
            }}, 2500);
        }}

        function getButtonCenterPosition(button) {{
            const rect = button.getBoundingClientRect();
            const containerRect = container.getBoundingClientRect();
            return {{
                x: rect.left - containerRect.left + rect.width / 2,
                y: rect.top - containerRect.top + rect.height / 2
            }};
        }}

        function selectButton(button) {{
            if (!selectedButtons.includes(button)) {{
                if (audioCtx && audioCtx.state === 'suspended') {{
                    audioCtx.resume();
                }}
                
                button.classList.add('selected');
                button.classList.remove('hover');
                
                selectedLetters.push(button.dataset.letter);
                selectedButtons.push(button);
                points.push(getButtonCenterPosition(button));
                updateSelectedWord();
                drawLine();
                playSelectSound();
            }}
        }}

        function clearAllSelections() {{
            document.querySelectorAll('.circle-button').forEach(button => {{
                button.classList.remove('selected');
                button.classList.remove('hover');
            }});
            selectedLetters = [];
            selectedButtons = [];
            points = [];
            updateSelectedWord();
            drawLine();
        }}

        function getButtonAtPosition(clientX, clientY) {{
            const buttons = document.querySelectorAll('.circle-button');
            let closestButton = null;
            let closestDistance = Infinity;
            
            buttons.forEach(button => {{
                if (!button.classList.contains('selected')) {{
                    button.classList.remove('hover');
                }}
            }});
            
            for (let button of buttons) {{
                const rect = button.getBoundingClientRect();
                const buttonCenterX = rect.left + rect.width / 2;
                const buttonCenterY = rect.top + rect.height / 2;
                
                const distance = Math.sqrt(
                    Math.pow(clientX - buttonCenterX, 2) + 
                    Math.pow(clientY - buttonCenterY, 2)
                );
                
                if (distance <= 30 && distance < closestDistance) {{
                    closestDistance = distance;
                    closestButton = button;
                }}
            }}
            
            if (closestButton && !closestButton.classList.contains('selected')) {{
                closestButton.classList.add('hover');
            }}
            
            return closestButton;
        }}

        function drawLine() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            if (points.length < 2) return;

            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);
            for (let i = 1; i < points.length; i++) {{
                ctx.lineTo(points[i].x, points[i].y);
            }}
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 2;
            ctx.stroke();

            points.forEach(point => {{
                ctx.beginPath();
                ctx.arc(point.x, point.y, 2, 0, 2 * Math.PI);
                ctx.fillStyle = '#333';
                ctx.fill();
            }});
        }}

        function handleMouseDown(event) {{
            event.preventDefault();
            const target = event.target;
            
            // ヒントターゲットがクリックされた場合は、ゲーム操作を開始しない
            if (target.closest('.word-hint-target')) {{
                return;
            }}
            
            isDragging = true;
            clearAllSelections();
            hideHint();
            
            const button = getButtonAtPosition(event.clientX, event.clientY);
            if (button) {{
                selectButton(button);
            }}
        }}

        function handleMouseMove(event) {{
            event.preventDefault();
            
            if (isDragging) {{
                const button = getButtonAtPosition(event.clientX, event.clientY);
                if (button) {{
                    selectButton(button);
                }}
            }} else {{
                getButtonAtPosition(event.clientX, event.clientY);
            }}
        }}

        function handleMouseUp(event) {{
            event.preventDefault();
            if (isDragging) {{
                isDragging = false;
                const isCorrect = checkCorrectWord();
                
                setTimeout(() => {{
                    clearAllSelections();
                }}, isCorrect ? 1000 : 200);
            }}
            document.querySelectorAll('.circle-button').forEach(button => {{
                button.classList.remove('hover');
            }});
        }}

        function handleTouchStart(event) {{
            event.preventDefault();
            const target = event.target;
            
            // ヒントターゲットがタッチされた場合は、ゲーム操作を開始しない
            if (target.closest('.word-hint-target')) {{
                return;
            }}
            
            isDragging = true;
            clearAllSelections();
            hideHint();
            
            const touch = event.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            if (button) {{
                selectButton(button);
            }}
        }}

        function handleTouchMove(event) {{
            event.preventDefault();
            if (!isDragging) return;
            
            const touch = event.touches[0];
            const button = getButtonAtPosition(touch.clientX, touch.clientY);
            if (button) {{
                selectButton(button);
            }}
        }}

        function handleTouchEnd(event) {{
            event.preventDefault();
            if (isDragging) {{
                isDragging = false;
                const isCorrect = checkCorrectWord();
                setTimeout(() => {{
                    clearAllSelections();
                }}, isCorrect ? 1000 : 200);
            }}
        }}

        // オーバーレイのボタンイベント
        nextStageBtn.addEventListener('click', function() {{
            hideStageCompleteOverlay();
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('next_stage', 'true');
            window.location.href = currentUrl.toString();
        }});

        backTitleBtn.addEventListener('click', function() {{
            hideStageCompleteOverlay();
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('back_to_title', 'true');
            window.location.href = currentUrl.toString();
        }});

        // オーバーレイ外をクリックしても閉じないように（必要に応じて有効化）
        // overlayDiv.addEventListener('click', function(e) {{
        //     if (e.target === overlayDiv) {{
        //         hideStageCompleteOverlay();
        //     }}
        // }});

        // ヒントポップアップをクリックで隠す機能
        hintPopupDiv.addEventListener('click', hideHint);
        hintPopupDiv.addEventListener('touchend', function(e) {{
            e.preventDefault();
            hideHint();
        }});

        // メインのゲームエリアをクリックした時にヒントを隠す
        container.addEventListener('click', function(e) {{
            if (!e.target.closest('.word-hint-target') && !e.target.closest('.hint-popup')) {{
                hideHint();
            }}
        }});

        document.addEventListener('mousedown', handleMouseDown);
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);

        document.addEventListener('touchstart', handleTouchStart, {{passive: false}});
        document.addEventListener('touchmove', handleTouchMove, {{passive: false}});
        document.addEventListener('touchend', handleTouchEnd, {{passive: false}});

        updateSelectedWord();
        updateTargetWordsDisplay();

        document.addEventListener('contextmenu', e => e.preventDefault());
        document.addEventListener('selectstart', e => e.preventDefault());
        </script>
    </body>
    </html>
    """

    components.html(html_content, height=450)
    
    # 次のステージへの遷移処理（JavaScript側から送信）
    query_params = st.query_params
    if "next_stage" in query_params:
        if st.session_state.current_stage < len(STAGES):
            st.session_state.current_stage += 1
            next_stage_info = STAGES[st.session_state.current_stage]
            st.session_state.target_words = next_stage_info['words']
            st.session_state.found_words = []
            st.session_state.temp_found_words = []
            # 新しいステージの文字をシャッフル
            stage_letters = next_stage_info['letters'].copy()
            random.shuffle(stage_letters)
            st.session_state.shuffled_letters = stage_letters
        st.query_params.clear()
        st.rerun()
    
    # タイトルに戻る処理（JavaScript側から送信）
    if "back_to_title" in query_params:
        st.session_state.game_state = 'title'
        st.query_params.clear()
        st.rerun()