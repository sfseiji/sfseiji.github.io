// AST121 promo video script trainer data
// FINAL script (2026-07-15): emailed version + 5 subtle edits for non-native spoken delivery.
// Edits validated by a 3-lens panel (JP-L1 phonetics / spoken rhythm / content fidelity) + adversarial verify.
window.TRAINER_DATA = {
  meta: {
    title: 'AST121 Promo Video Script',
    shoot: '2026-07-16T19:00:00-04:00',
    location: "J Robert S Prichard Alumni House, King's College Circle",
    targetSecondsMin: 75,
    targetSecondsMax: 95,
  },

  planHtml: `
  <b>今夜</b>
  <ol>
    <li>台本タブで修正点とカット割り（映像の流れ＝記憶の地図）を確認</li>
    <li>聞く: 通し2回（等速）→ シャドーイング1回（0.85x）</li>
    <li>暗記: 段落ごとに 全文 → 小語を隠す → 頭文字 まで上げる（P3 が最長・最優先）</li>
    <li>暗唱テスト: 段落ごとに採点 → 90% 超えたら通しを1回</li>
    <li>寝る直前に通しを1回（睡眠で定着する）</li>
  </ol>
  <b>明日</b>
  <ul>
    <li>朝: 通し採点2回。弱い段落だけ「頭文字/全部隠す」で復習 + 発音ドリル</li>
    <li>日中: 歩きながら暗唱（本番も歩きながら話す）。録音して聞き返す</li>
    <li>18時ごろ出発前: 本番モードで1回 → 何も見ずに通し2回</li>
  </ul>
  <b>本番 Tips（6/9 打ち合わせの内容より）</b>
  <ul>
    <li>ペースはゆっくりで OK。Philip は「15〜20秒伸びても大丈夫、むしろ間を取れる」と明言済み</li>
    <li>複数テイク前提。噛んだら止まらず、その文の頭から言い直せば編集で切れる</li>
    <li>カメラ目線が要るのは3箇所だけ: 名乗り (P2)・コースのピッチ (P4)・締め (P6)。ここは笑顔＋目線</li>
    <li>script の微修正（rural → countryside など）は撮影前に Philip へ一言伝えると安全（この行で京都の映像にカットする計画のため。内容・カット割りは不変）</li>
    <li>天候・煙の最終確認は Philip がメールスレッドに返信（当日はテキスト/WhatsApp で連絡）</li>
  </ul>`,

  changes: [
    {
      original: 'among the mountains of rural Kyoto',
      replacement: 'among the mountains of the Kyoto countryside',
      why: 'rural は r→l 切替が2回入る英語最難級の語（3視点すべてが最重要指摘）。countryside は馴染みのある易しい語で、田舎育ちの事実と映像プランはそのまま。',
    },
    {
      original: 'And it is that same spark that now sends me chasing…',
      replacement: 'And that same spark now sends me chasing…',
      why: '書き言葉的な強調構文（it is X that…）を解消。直前の That same curiosity once made me… と完全に並行になり、覚えやすく、歩きながらの一息で言い切れる。',
    },
    {
      original: 'That is what AST121…',
      replacement: "That's what AST121…",
      why: '話し言葉の自然な短縮形。コースタイトルへの助走が軽くなる（タイトル自体は一字も変更なし）。',
    },
    {
      original: 'It is built for curious…',
      replacement: "It's built for curious…",
      why: '段落頭の It is は音読っぽく聞こえる。会話の標準形へ。',
    },
    {
      original: 'If you have ever wondered…',
      replacement: "If you've ever wondered…",
      why: '締めの一文が「読んでいる」でなく「話している」に聞こえる。CTA 部分は無変更。',
    },
  ],

  paragraphs: [
    {
      label: 'Hook（2つの問い）', cue: 'Where…? How…?', camera: 'vo',
      visual: 'Big Bang→銀河・星→生命のタイムラプス',
      deliveryNote: 'ゆっくり・低めに、問いかけるように。wh疑問文なので文末は下げ調で着地。',
      text: 'Where did the Universe come from? How did galaxies, stars, and even life itself emerge?',
      sentences: [
        'Where did the Universe come from?',
        'How did galaxies, stars, and even life itself emerge?',
      ],
    },
    {
      label: '自己紹介（名前・京都）', cue: "I'm Seiji…", camera: 'on',
      visual: '歩いて登場（名乗り）→ 京都の山里の映像へ',
      deliveryNote: '名乗りはカメラ目線＋笑顔。ここが第一印象。"Toronto," のコンマで小さく息継ぎしてから I grew up へ。',
      text: "I'm Seiji Fujimoto, a new faculty member at the University of Toronto, and I grew up among the mountains of the Kyoto countryside, where curiosity got the better of me early on.",
      sentences: [
        "I'm Seiji Fujimoto, a new faculty member at the University of Toronto, and I grew up among the mountains of the Kyoto countryside, where curiosity got the better of me early on.",
      ],
    },
    {
      label: 'Curiosity（核心段落）', cue: "I've come to believe…", camera: 'vo',
      visual: '京都 → Double Dutch 映像 → JWST',
      deliveryNote: '一番熱を込める段落。"move us" と "wonder" を立てる。champion で少し笑って良い。最後の文は少しゆっくり。',
      text: "I've come to believe curiosity is one of the things that makes us most human. We don't live for comfort or efficiency; we live for the things that move us, the things that make us wonder. That same curiosity once made me a Double Dutch world champion, just by chasing whatever lit me up inside. And that same spark now sends me chasing the first galaxies with the James Webb Space Telescope.",
      sentences: [
        "I've come to believe curiosity is one of the things that makes us most human.",
        "We don't live for comfort or efficiency; we live for the things that move us, the things that make us wonder.",
        'That same curiosity once made me a Double Dutch world champion, just by chasing whatever lit me up inside.',
        'And that same spark now sends me chasing the first galaxies with the James Webb Space Telescope.',
      ],
    },
    {
      label: 'コースのピッチ', cue: "That's what AST121…", camera: 'on',
      visual: 'ピッチは顔出し → トピック列挙は映像（Big Bang・dark matter・ブラックホール）',
      deliveryNote: 'ピッチはカメラ目線。タイトルはコンマで間を取りながら1語ずつ。列挙は1項目ずつ等リズムで。',
      text: 'That\'s what AST121, "Twinkle, Sparkle, Brilliant Sky," is really about. We won\'t just memorize facts. We will explore the modern Universe through its biggest open questions: the Big Bang, dark matter, black holes, the first galaxies, and the search for life.',
      sentences: [
        'That\'s what AST121, "Twinkle, Sparkle, Brilliant Sky," is really about.',
        "We won't just memorize facts.",
        'We will explore the modern Universe through its biggest open questions: the Big Bang, dark matter, black holes, the first galaxies, and the search for life.',
      ],
    },
    {
      label: '誰のための講義か', cue: "It's built for…", camera: 'vo',
      visual: '宇宙全体へズームアウト',
      deliveryNote: '落ち着いて。"whole" は h から（w は発音しない）。',
      text: "It's built for curious first-year science students who want to see the Universe as a whole.",
      sentences: [
        "It's built for curious first-year science students who want to see the Universe as a whole.",
      ],
    },
    {
      label: '締め（CTA）', cue: "If you've ever wondered…", camera: 'on',
      visual: '最後は顔出しで締め',
      deliveryNote: 'ひと呼吸置いてから、にこやかに言い切る。"come find out with us" は fin-DOUT に山を置いてゆっくり。',
      text: "If you've ever wondered where everything comes from, come find out with us.",
      sentences: [
        "If you've ever wondered where everything comes from, come find out with us.",
      ],
    },
  ],

  // Verified by drill-build + phonetician-verify agents (2026-07-15).
  drills: {
    words: [
      { word: 'Universe', ipa: '/ˈjunəˌvɝs/', stress: 'YU-ni-verse', category: 'V/W/F', tip_ja: '「ユニバース」の「バ」は /v/。下唇を上の歯に軽く当てて濁らせる。語尾は「ース」と伸ばさず、舌を巻いた /ɝs/ で締める。強勢は先頭の YU だけ、後ろは弱く流す。' },
      { word: 'galaxies', ipa: '/ˈɡæləksiz/', stress: 'GA-la-xies', category: 'cluster', tip_ja: '「ギャラクシーズ」だと拍が多すぎる。3音節で GA だけ強く。/æ/ は「ガ」と「ギャ」の中間で口を横に開く。/ks/ の間に母音を入れず、語尾 /siz/ は弱く一気に。' },
      { word: 'emerge', ipa: '/ɪˈmɝdʒ/', stress: 'e-MERGE', category: 'vowel', tip_ja: '強勢は2音節目。「イマージ」ではなく /mɝdʒ/：舌を巻いた r 色母音のまま /dʒ/ で終える。最後に「ジー」と母音を足さない。頭の e は弱い /ɪ/ で軽く。' },
      { word: 'faculty', ipa: '/ˈfækəlti/', stress: 'FA-cul-ty', category: 'cluster', tip_ja: '「ファカルティ」の「ル」を母音化しない。/kəl/ は舌先を歯茎に付けるだけの暗いLで、すぐ /ti/ へ。3音節で FA だけ立てる。f は下唇+上歯。' },
      { word: 'Toronto', ipa: '/təˈrɑntoʊ/', stress: 'to-RON-to', category: 'stress', tip_ja: '強勢は真ん中の RON。第1音節は曖昧母音で「タ」程度に潰す。現地発音は2つ目の t が落ちて「トゥラーノ」に近い。「トロント」と3拍平板に言うと一発で非ネイティブに聞こえる。' },
      { word: 'curiosity', ipa: '/ˌkjʊriˈɑsəti/', stress: 'cu-ri-OS-i-ty', category: 'stress', tip_ja: '5音節で山は OS だけ。「キュリオシティ」と全拍均等にせず、OS を高く長く、前後は転がす。/ɑ/ は口を大きく開ける。t はフラップ（軽いラ行の d）でOK。この script の主役の語なので特に反復を。' },
      { word: 'mountains', ipa: '/ˈmaʊntənz/', stress: 'MOUN-tains', category: 'vowel', tip_ja: '「マウンテンズ」の「テ」は無い。GAでは t が喉で止まる音になり「マウンʔンズ」。2音節目は曖昧母音+n で弱く。二重母音 /aʊ/ をしっかり「アゥ」と動かす。' },
      { word: 'countryside', ipa: '/ˈkʌntriˌsaɪd/', stress: 'COUN-try-side', category: 'stress', tip_ja: '今回の修正で入った語（rural の代わり）。「カントリーサイド」7拍→3音節に圧縮。COUN に主強勢、-side は二重母音 /aɪ/ で締め、d の後に母音を足さない。' },
      { word: 'believe', ipa: '/bɪˈliv/', stress: 'be-LIEVE', category: 'R/L', tip_ja: 'L は舌先を上歯茎にしっかり付ける（r 化させない）。語尾 /v/ は下唇+上歯で止めて「ブ」と母音を足さない。「ビリーブ」でなく be は弱く、LIEVE に山。' },
      { word: 'comfort', ipa: '/ˈkʌmfɚt/', stress: 'COM-fort', category: 'vowel', tip_ja: '「コンフォート」と伸ばさない。2音節目は /fɚt/：弱い r 色母音+t で短く。強勢は /kʌm/。速く言うなら「カムファト」のイメージで、オーを消すのがコツ。' },
      { word: 'efficiency', ipa: '/ɪˈfɪʃənsi/', stress: 'ef-FI-cien-cy', category: 'stress', tip_ja: '強勢は FI。頭は弱い /ɪ/ で軽く入る。「エフィシェンシー」と全部強く言わず、FI だけ立てて後半 /ʃənsi/ は一息で流す。f は下唇+上歯。comfort or efficiency の対句でリズム練習を。' },
      { word: 'wonder', ipa: '/ˈwʌndɚ/', stress: 'WON-der', category: 'V/W/F', tip_ja: 'w は唇をすぼめて丸めてから開く（日本語の「ワ」では弱い）。母音は /ʌ/ で短く「ワ」でなく「ゥア」。「ワンダー」と伸ばさず /dɚ/ で軽く舌を巻いて終える。' },
      { word: 'world', ipa: '/ˈwɝld/', stress: 'WORLD (1音節)', category: 'R/L', tip_ja: '最難関。「ワールド」の4拍を1音節に圧縮：唇を丸めた w → 舌を巻く /ɝ/ → 舌先を歯茎に付ける暗いL → 軽い d。ラ行を入れず「ウァ〜ゥ(ル)ド」。速い時は d をほぼ落として次語へ移ってよい。' },
      { word: 'champion', ipa: '/ˈtʃæmpiən/', stress: 'CHAM-pi-on', category: 'vowel', tip_ja: '「チャンピオン」の5拍でなく3音節。/tʃæm/ に強勢を置き、後半 /piən/ は「ピァン」と弱く一息。/æ/ は口を横に開く。オ段の「オン」を出さない。' },
      { word: 'chasing', ipa: '/ˈtʃeɪsɪŋ/', stress: 'CHA-sing', category: 'vowel', tip_ja: '母音は二重母音 /eɪ/：「チェー」と伸ばさず「チェイ」と動かす。語尾 /ŋ/ は鼻に抜くだけで g や「グ」を出さない。script に2回出る動詞なので要チェック。' },
      { word: 'spark', ipa: '/ˈspɑrk/', stress: 'SPARK (1音節)', category: 'cluster', tip_ja: '頭の s に母音を入れない（「ス」禁止、s は息だけ）。/pɑr/ は口を大きく開けて r へ。最後の k は軽く止めるだけで「ク」と言わない。「スパーク」4拍→1音節へ。' },
      { word: 'Webb', ipa: '/ˈwɛb/', stress: 'WEBB (1音節)', category: 'V/W/F', tip_ja: '「ウェッブ」でなく短く /wɛb/。w で唇をしっかり丸めてから /ɛ/ へ。語尾 b は唇を閉じて止め、「ブ」の母音を足さない。直後の Space の s へすぐ移る練習を。' },
      { word: 'telescope', ipa: '/ˈtɛləˌskoʊp/', stress: 'TE-le-scope', category: 'R/L', tip_ja: '強勢は先頭 TE。中の l は舌先を軽くタッチ（「レ」のラ行でごまかさない）。/skoʊp/ は「スコープ」と伸ばさず二重母音 /oʊ/、最後は唇を閉じる p で母音なし。' },
      { word: 'Twinkle', ipa: '/ˈtwɪŋkəl/', stress: 'TWIN-kle', category: 'cluster', tip_ja: '/tw/ は t を出した直後に唇を丸める。「トゥイ」と2拍にせず一瞬で。語尾 /kəl/ は暗いL：「クル」と言わず、k の後に舌先を歯茎に付けて終わる。' },
      { word: 'Sparkle', ipa: '/ˈspɑrkəl/', stress: 'SPAR-kle', category: 'R/L', tip_ja: 'spark と同じ入りに /kəl/ が付く形。R（舌を巻く）→ L（舌先を付ける）の切替が核心。「スパークル」の5拍を2音節に。R と L を同じラ行にしないこと。' },
      { word: 'Brilliant', ipa: '/ˈbrɪljənt/', stress: 'BRIL-liant', category: 'R/L', tip_ja: '2音節だけ。「ブリリアント」の6拍にしない。/br/ は「ブ」の母音を入れずに r へ。中央は /lj/：L で舌先を付けてから y に滑って「リィヤント」。1語の中で R→L が出る難所。' },
      { word: 'really', ipa: '/ˈrili/', stress: 'REAL-ly', category: 'R/L', tip_ja: 'r で始まり l で終わる難所（タイトル直後の重要文に登場）。r は舌をどこにも付けず、l は舌先を歯茎へ。「リアリー」より軽く /ˈrili/。多少崩れても通じるので、タイトルを立てて really は弱く流す。' },
      { word: 'memorize', ipa: '/ˈmɛməˌraɪz/', stress: 'ME-mo-rize', category: 'R/L', tip_ja: '強勢は先頭 ME。真ん中の r は舌をどこにも付けずに巻く（ラ行の「ラ」にしない）。語尾 /aɪz/ の z の後に母音を足さない。「メモライズ」の平板読み回避。' },
      { word: 'explore', ipa: '/ɪkˈsplɔr/', stress: 'ex-PLORE', category: 'cluster', tip_ja: '/kspl/ の4連続子音に母音を挟まない。「エクスプロア」の各拍を潰し、ex は弱く一瞬、PLORE に山。/ɔr/ は口を丸めて r で締め、「ア」を最後に足さない。' },
      { word: 'modern', ipa: '/ˈmɑdɚn/', stress: 'MO-dern', category: 'vowel', tip_ja: '「モダン」ではない。第1音節は /mɑ/ で口を大きく開けて「マー」に近い。2音節目は /dɚn/：d の直後に舌を巻いて n へ。「モ」と「ダン」どちらのカタカナ母音も違う。' },
      { word: 'through', ipa: '/ˈθru/', stress: 'THROUGH (1音節)', category: 'TH', tip_ja: '舌先を軽く歯に挟んで息を出し（無声 th）、すぐ舌を引いて r → /u/ へ。「スルー」（s 発音）にも「ツルー」にもしない。th が崩れるくらいなら弱い t の方がまだ自然。' },
      { word: 'holes', ipa: '/ˈhoʊlz/', stress: 'HOLES (1音節)', category: 'final-consonant', tip_ja: '「ホールズ」と伸ばさず1音節。二重母音 /oʊ/「ホウ」→ 舌先を歯茎に付ける暗いL → z。最後に「ズ」の母音を足さない。whole と同じ母音+L。' },
      { word: 'first-year', ipa: '/ˈfɝst ˈjɪr/', stress: 'FIRST-year', category: 'vowel', tip_ja: 'first は /ɝst/：巻き舌母音+st を1音節で（「ファースト」4拍禁止）。year は頭に /j/ を入れる：「イヤー」だと ear になる。ヤ行の構えから /jɪr/。複合語として両方やや強く。' },
      { word: 'science', ipa: '/ˈsaɪəns/', stress: 'SCI-ence', category: 'final-consonant', tip_ja: '2音節 /saɪ-əns/。「サイエンス」の「エ」は弱い曖昧母音に潰す。語尾 /ns/ は n から s へ直結し「ンス」の母音を入れない。次の students の s と繋がる位置なので語尾処理が重要。' },
      { word: 'whole', ipa: '/ˈhoʊl/', stress: 'WHOLE (1音節)', category: 'final-consonant', tip_ja: 'wh でも w は発音せず /h/ から。「ホール」と伸ばさず二重母音 /oʊ/「ホウ」、最後は暗いLで舌先を歯茎へ。「ル」と言わずに舌を付けるだけ。as a whole の文末で目立つ語。' },
      { word: 'early', ipa: '/ˈɝli/', stress: 'EAR-ly', category: 'R/L', tip_ja: 'R→L 切替の代表ドリル。/ɝ/ で舌を巻いて浮かせたまま → /li/ で舌先を歯茎にタッチ。「アーリー」とラ行1本でごまかすと r も l も消える。ゆっくり「ァ〜(巻く)・リ(付ける)」から加速。' },
    ],
    phrases: [
      { text: 'lit me up inside', focus: 'linking', tip_ja: 'lit の t は飲み込んで li(t)-me、up は inside と繋げて u-PIN-side：「リッミー・アッピンサイド」。山は最後の SIDE。t をきっちり「リット」と発音すると流れが死ぬ。' },
      { text: 'come find out with us', focus: 'linking', tip_ja: 'find の d を out に渡して fin-DOUT、with と us も繋げて wi-THUS：「カム・ファインダウト・ウィザス」。find out を1語のように。締めの一文なので、DOUT に山を置いて言い切る。' },
      { text: 'got the better of me early on', focus: 'rhythm', tip_ja: '立てるのは got / BE-tter / EAR-ly / ON だけ。better of は t をフラップ化して BE-də-rəv、of me は弱形で「アヴミ」。early は on と繋げて EAR-ly‿ON。機能語を潰すほどネイティブのリズムに近づく。' },
      { text: 'one of the things that makes us most human', focus: 'rhythm', tip_ja: 'one of the は「ワナダ」と一塊の弱形（WA-nə-ðə）。that は /ðət/ に潰す。makes us は MAY-k‿SUS と連結。山は one / THINGS / MAKES / MOST / HU-man。th が3箇所（the と that は有声 /ð/、things だけ無声 /θ/）あるので舌先を歯に。' },
      { text: 'Twinkle, Sparkle, Brilliant Sky', focus: 'cluster', tip_ja: '講義タイトル＝一番決めたい所。TWIN-kl / SPAR-kl / BRIL-lyənt と語尾に母音を足さず、コンマで軽く間を取り、SKY を上げて着地。L語尾2連発→R+L 切替と続く難所なので、ゆっくり3回→通常速度の順で。' },
      { text: 'James Webb Space Telescope', focus: 'stress', tip_ja: 'JAMES / WEBB / SPACE / TE-lescope と頭打ちの4連強勢。James の /mz/ から Webb の w へ唇を素早く丸め直すのが難所。Space は頭の s に母音を入れず /speɪs/。「ジェームズウェッブ」と平板にせず1語ずつ叩く。' },
      { text: 'black holes', focus: 'cluster', tip_ja: 'BLACK ／ HOLES と2拍で叩く。bl は「ブ」の母音を入れず一気に l へ。black の k は軽く止めるだけで holes に繋ぐ。holes は /hoʊlz/：「ホールズ」と伸ばさず二重母音「ホウ」→暗いL→z。列挙の1項目として等リズムで。' },
      { text: 'Double Dutch world champion', focus: 'cluster', tip_ja: 'DOU-ble DUTCH は D の頭韻をはっきり2発。world は1音節 /wɝld/ のまま champion へ：「ワールドチャンピオン」の9拍を 1+3音節に圧縮。world の d は軽く止めるだけで、すぐ /tʃ/ に移ると自然に繋がる。' },
      { text: 'first-year science students', focus: 'cluster', tip_ja: '/st/ の連発地帯：fir-ST / STu-dents。science と students は s 同士を繋げて SCI-ence‿STU-dents、間に母音を挟まない。first-year は複合語として両方立てる。students の語尾 /nts/ も「ツ」と母音を足さず止める。' },
      { text: 'through its biggest open questions', focus: 'cluster', tip_ja: 'through は /θru/：舌先を歯に軽く挟んで息→すぐ舌を引いて r へ（「スルー」禁止）。its biggest は ts→b を止めてから弾む。山は BIG-gest / O-pen / QUES-tions。questions は /ˈkwɛstʃənz/ で「クエスチョンズ」と平板にしない。' },
      { text: 'a new faculty member at the University of Toronto', focus: 'rhythm', tip_ja: '機能語 a / at the / of は全部弱形（ə / ət-ðə / əv）。University of Toronto は「ユニヴァーサティアヴ・タラーノ」と一続きに（U-ni-VER-si-ty‿əv‿tə-RON-to）。山は NEW / FA- / MEM- / -VER- / -RON-。自己紹介文なので暗唱レベルまで。' },
      { text: 'Where did the Universe come from?', focus: 'rhythm', tip_ja: '冒頭の一文。wh疑問文なので文末は下げ調で終える（上げない）。did the は「ディダ」と潰し、山は WHERE / U-niverse / COME。from は文末でも弱形 /frəm/ のまま低く着地。開幕なのでゆっくり・低めに始めると映像映えする。' },
    ],
  },

  // Expression / 抑揚ガイド: どこを強く(emph=太字)、どう上げ下げ・間を取るか(arc)。
  // 機械音声の平坦さを抜けて「パッションが伝わる」抑揚を自分で乗せるための手本メモ。
  expression: {
    '0_0': { emph: ['Where', 'Universe', 'come'], arc: 'ゆっくり低めに入る。wh疑問なので文末は ↘。Universe を少し長く。' },
    '0_1': { emph: ['galaxies', 'stars', 'life', 'emerge'], arc: 'galaxies ／ stars ／ life と区切って ↗、emerge で ↘ 着地。開幕の余韻を残す。' },
    '1_0': { emph: ['Seiji Fujimoto', 'Toronto', 'countryside', 'curiosity'], arc: '名乗りは笑顔で明るく ↗。Toronto, で／ひと呼吸。後半 curiosity got the better of me は茶目っ気を込めて軽く ↘。' },
    '2_0': { emph: ['believe', 'curiosity', 'human'], arc: '確信を込めて。most human を強くゆっくり ↘ で言い切る。' },
    '2_1': { emph: ["don't", 'comfort', 'efficiency', 'move', 'wonder'], arc: '前半 comfort or efficiency は突き放して ↘。; の後は温かく ↗。move us と wonder を立て、wonder で余韻。' },
    '2_2': { emph: ['Double', 'Dutch', 'champion', 'chasing', 'lit'], arc: '誇らしげに、少し笑って。world champion で ↗ ピーク。chasing whatever lit me up inside は勢いよく畳みかける。' },
    '2_3': { emph: ['spark', 'first', 'galaxies', 'James', 'Webb'], arc: 'spark を受けて加速 ↗。first galaxies を高く、James Webb Space Telescope は1語ずつ叩いて ↘ 決める。' },
    '3_0': { emph: ['AST121', 'Twinkle', 'Sparkle', 'Brilliant', 'really'], arc: 'カメラ目線で誇らしく。タイトルは／間を取り1語ずつ、Brilliant Sky ↗、really about で ↘。' },
    '3_1': { emph: ["won't", 'memorize'], arc: 'きっぱり短く ↘。次の文との対比なので低めに置く。' },
    '3_2': { emph: ['explore', 'questions', 'Bang', 'matter', 'holes', 'galaxies', 'life'], arc: 'explore で ↗ 開く。: の後は列挙、1つずつ／等間隔で少し上げ、search for life で ↘ 締める。' },
    '4_0': { emph: ['curious', 'first-year', 'whole'], arc: '落ち着いて温かく。curious を優しく、the Universe as a whole は ↘ ゆっくり。' },
    '5_0': { emph: ['wondered', 'everything', 'find', 'us'], arc: 'ひと呼吸おいて始める。前半は ↗ 誘いかけ、come find out with us は笑顔でゆっくり ↘ 言い切る。' },
  },

  // Word popups in the Script tab. Built from drills.words below; extras added manually.
  hardWords: {},
};

// Build hardWords from verified drill data (keys must match the app's normWord()).
(function () {
  const D = window.TRAINER_DATA;
  const norm = w => w.toLowerCase().replace(/[’]/g, "'").replace(/[^a-z0-9']/g, '');
  for (const w of D.drills.words) {
    D.hardWords[norm(w.word)] = { word: w.word, ipa: w.ipa, stress: w.stress, tip: w.tip_ja };
  }
  // extras not in the drill deck but worth a popup
  Object.assign(D.hardWords, {
    human: { word: 'human', ipa: '/ˈhjumən/', stress: 'HU-man', tip: 'hj の連続（ヒュ）で入り、-man は弱く /mən/。「ヒューマン」と後ろを立てない。' },
    wondered: { word: 'wondered', ipa: '/ˈwʌndɚd/', stress: 'WON-dered', tip: '語末 -ed は /d/ 一拍だけ。「ワンダード」と伸ばさない。w は唇を丸めて。' },
    questions: { word: 'questions', ipa: '/ˈkwɛstʃənz/', stress: 'QUES-tions', tip: 'kw で唇を丸める。-tions は /tʃənz/ で「チョンズ」と平板にせず弱く。' },
    students: { word: 'students', ipa: '/ˈstudənts/', stress: 'STU-dents', tip: '頭の st に母音を入れない。語尾 /nts/ は「ツ」と言わず止める。' },
    everything: { word: 'everything', ipa: '/ˈɛvriˌθɪŋ/', stress: 'EV-ery-thing', tip: 'v は下唇+上歯。-thing は無声 th /θɪŋ/ で「シング」にしない。' },
  });
})();
