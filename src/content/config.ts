import { defineCollection, z } from 'astro:content';

const vault = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    description: z.string().optional(),
    link: z.string().url().optional(),
    category: z.enum(['news', 'blog', 'cnk', 'cvut', 'zleb']).default('news'),
    isMilestone: z.boolean().default(false),
  }),
});

export const collections = {
  vault,
};
