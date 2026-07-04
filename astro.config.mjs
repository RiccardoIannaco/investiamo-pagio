import { defineConfig } from 'astro/config';

// Su GitHub Actions GITHUB_REPOSITORY vale "proprietario/repo": site e base
// si adattano da soli al nome del repo. In locale si usa il fallback.
const [proprietario, repo] = (process.env.GITHUB_REPOSITORY ?? 'locale/investiamo-pagio').split('/');

export default defineConfig({
  site: `https://${proprietario}.github.io`,
  base: `/${repo}`,
});
