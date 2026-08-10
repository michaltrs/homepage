import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const vault = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/vault' }),
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    description: z.string().optional(),
    link: z.string().optional(),
    category: z.enum(['news', 'blog', 'cnk', 'cvut-fel', 'spse-v-uzlabine']).default('news'),

    isMilestone: z.boolean().default(false),
  }),
});

export const collections = {
  vault,
};
