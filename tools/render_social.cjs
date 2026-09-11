/* Usage: node tools/render_social.cjs. Install sharp or set CODEX_PRIMARY_RUNTIME_NODE_MODULES. */
const path = require('node:path');
const fs = require('node:fs/promises');
const sharp = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
  ? path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, 'sharp') : 'sharp');
const root = path.resolve(__dirname, '..');
(async () => {
  const directory = path.join(root, 'assets/social');
  for (const name of (await fs.readdir(directory)).filter(name => name.endsWith('.svg'))) {
    await sharp(path.join(directory, name)).png({ compressionLevel: 9 })
      .toFile(path.join(directory, name.replace('.svg', '.png')));
  }
})();
