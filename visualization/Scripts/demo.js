// Load the bundled match when opened through the public demo entry point.
(async function () {
  if (!new URLSearchParams(window.location.search).has('demo')) return;

  const input = fileChooser.nextElementSibling;
  input.disabled = true;
  fileChooser.textContent = '正在载入示例比赛……';
  try {
    const response = await fetch('../data/replay1.json');
    if (!response.ok) throw new Error(`Replay request failed: ${response.status}`);
    const record = await response.json();
    if (!Array.isArray(record.frames) || !record.frames.length || !record.scores) {
      throw new Error('Incomplete demo replay');
    }
    record.teamNames = ['第13组策略', '贪心基线'];
    initialization(record);
    updateChooser(fileChooser);
  } catch (error) {
    input.disabled = false;
    fileChooser.textContent = '示例载入失败，点击选择本地比赛记录';
    console.error(error);
  }
})();
