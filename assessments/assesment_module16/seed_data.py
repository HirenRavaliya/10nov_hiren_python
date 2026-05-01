"""
Seed script: Creates demo data for WriteSphere.
Run with: python manage.py shell < seed_data.py
  OR:      python seed_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'writesphere.settings')
django.setup()

from django.contrib.auth.models import Group
from accounts.models import CustomUser, Follow
from blog.models import Category, Tag, Post

# =============================================
# GROUPS — Admin, Author, Reader
# =============================================
admin_group, _ = Group.objects.get_or_create(name='Admin')
author_group, _ = Group.objects.get_or_create(name='Author')
reader_group, _ = Group.objects.get_or_create(name='Reader')
print('✓ Groups created: Admin, Author, Reader')

# Categories
cats = ['Technology', 'Design', 'Business', 'Science', 'Culture', 'Travel', 'Health']
cat_objects = {}
for name in cats:
    c, _ = Category.objects.get_or_create(name=name)
    cat_objects[name] = c
print('✓ Categories created')

# Tags
tag_names = ['python', 'django', 'webdev', 'design', 'productivity', 'startup', 'ai', 'writing', 'leadership', 'creativity']
tag_objects = {}
for name in tag_names:
    t, _ = Tag.objects.get_or_create(name=name)
    tag_objects[name] = t
print('✓ Tags created')

# Superuser / admin
if not CustomUser.objects.filter(username='admin').exists():
    admin = CustomUser.objects.create_superuser(
        username='admin',
        email='admin@writesphere.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        bio='Platform administrator and avid blogger.'
    )
    print('✓ Admin user created (admin / admin123)')
else:
    admin = CustomUser.objects.get(username='admin')
    print('✓ Admin user already exists')
# Admin group (informational — is_staff already grants full access)
admin.groups.add(admin_group)

# Demo authors
demo_users_data = [
    ('alice', 'alice@example.com', 'alice123', 'Alice', 'Chen', 'Full-stack developer and open source enthusiast. I write about Python, Django, and modern web development.'),
    ('bob', 'bob@example.com', 'bob123', 'Bob', 'Martinez', 'Product designer with a love for minimalism and user-centered design.'),
    ('carol', 'carol@example.com', 'carol123', 'Carol', 'Williams', 'Entrepreneur and startup advisor. Sharing insights on building products people love.'),
]

demo_users = {}
for uname, email, pwd, fn, ln, bio in demo_users_data:
    if not CustomUser.objects.filter(username=uname).exists():
        u = CustomUser.objects.create_user(
            username=uname, email=email, password=pwd,
            first_name=fn, last_name=ln, bio=bio
        )
        demo_users[uname] = u
    else:
        demo_users[uname] = CustomUser.objects.get(username=uname)
    # Ensure all demo authors are in the Author group
    demo_users[uname].groups.add(author_group)
print('✓ Demo Authors created/updated: alice, bob, carol')

# Demo Reader user
if not CustomUser.objects.filter(username='reader').exists():
    reader_user = CustomUser.objects.create_user(
        username='reader',
        email='reader@example.com',
        password='reader123',
        first_name='Sam',
        last_name='Reader',
        bio='An avid reader who loves discovering great content on WriteSphere.'
    )
    reader_user.groups.add(reader_group)
    print('✓ Demo Reader created (reader / reader123)')
else:
    reader_user = CustomUser.objects.get(username='reader')
    reader_user.groups.add(reader_group)
    print('✓ Demo Reader already exists')

# Follow relationships
for follower_name, following_name in [('alice', 'bob'), ('bob', 'carol'), ('carol', 'alice'), ('admin', 'alice')]:
    f = demo_users.get(follower_name) or admin
    t = demo_users.get(following_name) or admin
    Follow.objects.get_or_create(follower=f, following=t)
print('✓ Follow relationships created')

# Demo posts
posts_data = [
    {
        'title': 'Getting Started with Django: A Complete Guide for 2024',
        'author': 'alice',
        'category': 'Technology',
        'tags': ['python', 'django', 'webdev'],
        'content': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

Django follows the Model-View-Template (MVT) architectural pattern, which is similar to the Model-View-Controller (MVC) pattern used by many other frameworks.

Getting started with Django is surprisingly straightforward. After installing Python and pip, you can install Django with a simple pip command and have a working project skeleton in minutes.

The Django ORM (Object-Relational Mapper) deserves special mention. It allows you to interact with your database using Python code instead of SQL, making database operations intuitive and readable.

Authentication, admin panels, URL routing, form handling — Django provides all of these out of the box. This "batteries included" philosophy is what makes it so productive for building complex web applications quickly.

Whether you're building a simple blog or a complex enterprise application, Django scales beautifully and has a rich ecosystem of third-party packages to extend its capabilities.''',
    },
    {
        'title': 'The Art of Minimalist Design: Less Is More',
        'author': 'bob',
        'category': 'Design',
        'tags': ['design', 'creativity'],
        'content': '''Minimalism in design isn't about removing things for the sake of removing them. It's about finding the essential core of what you're trying to communicate and presenting it with clarity and purpose.

The best minimalist designs aren't empty — they're focused. Every element earns its place. White space isn't wasted space; it's breathing room that gives importance to what remains.

Typography becomes crucial in minimalist design. When you strip away decorative elements, the quality of your type choices is exposed. A well-chosen typeface can carry enormous expressive weight.

Color takes on a different role, too. In a minimalist palette, each color choice ripples through the entire composition. Neutrals become powerful, and accent colors — when used — become dramatic punctuation marks.

The challenge of minimalist design is knowing what to cut. It requires a deep understanding of the user's goals and a willingness to ruthlessly eliminate anything that doesn't serve those goals directly.''',
    },
    {
        'title': 'Building a Startup in 2024: Lessons from the Trenches',
        'author': 'carol',
        'category': 'Business',
        'tags': ['startup', 'leadership', 'productivity'],
        'content': '''Launching a startup is one of the most exhilarating and humbling experiences you can have as an entrepreneur. After founding three companies and advising dozens of others, I've learned that the path to success is rarely linear.

The first lesson: validate before you build. Too many founders fall in love with their solution before truly understanding the problem. Talk to potential customers obsessively before writing a single line of code.

Product-market fit — that magical moment when your product resonates deeply with a specific market — is both harder to achieve and easier to feel than most people expect. When you have it, growth feels effortless. When you don't, everything is a struggle.

Team composition matters enormously. The best idea executed by a mediocre team will be beaten by a good idea executed by an exceptional team. Prioritize people who are intellectually curious, resilient, and genuinely invested in the mission.

Cash is oxygen. Understanding your burn rate and runway isn't just accounting — it's strategic awareness. Give yourself enough time to learn and iterate before you need to raise or generate revenue.''',
    },
    {
        'title': 'Why I Switched from React to Django Templates',
        'author': 'alice',
        'category': 'Technology',
        'tags': ['django', 'webdev', 'python'],
        'content': '''For three years, I built every frontend in React. It was the default choice — everyone was using it, there were tons of libraries, and it felt modern. But somewhere along the way, I started questioning whether all that complexity was actually serving my projects.

The turning point came when I was building a content platform with Django as the backend. I had set up Django REST Framework and was building a separate React frontend when I had a realization: 90% of what I needed was just server-rendered HTML with some sprinkles of JavaScript.

Django's template system is genuinely powerful. Template inheritance, custom template tags, the `with` tag — these cover most real-world UI needs elegantly. And when I need interactivity, a small amount of vanilla JavaScript or HTMX handles it beautifully.

The benefits were immediate. Fewer dependencies to maintain. Faster initial page loads. Simpler deployment. Better SEO out of the box. And one codebase instead of two.

I'm not saying React is bad — it's the right tool for highly interactive SPAs. But for content sites, blogs, dashboards, and most business applications, Django templates with a touch of JavaScript is often a better fit than a full SPA architecture.''',
    },
    {
        'title': 'The Power of Deep Work in a Distracted World',
        'author': 'bob',
        'category': 'Culture',
        'tags': ['productivity', 'creativity', 'writing'],
        'content': '''Cal Newport's concept of "deep work" — the ability to focus without distraction on a cognitively demanding task — feels increasingly rare and increasingly valuable.

In an era of constant notifications, open offices, and the glorification of busyness, the ability to sit quietly and think deeply for hours at a time is practically a superpower.

I've been deliberately practicing deep work for two years now. The results have been transformative. Projects that used to take weeks now take days. The quality of my thinking has improved noticeably.

The key practices that have worked for me: scheduling deep work blocks in the morning when my mental energy is highest, turning off all notifications during those blocks, and treating my deep work schedule as sacred as any meeting.

The shallow work — emails, Slack messages, administrative tasks — gets batched into the afternoon. It still gets done, but it doesn't crowd out the work that actually matters.

Digital minimalism has been a crucial complement. The fewer apps and services competing for my attention, the easier it is to be present in my work.''',
    },
]

for pd in posts_data:
    author = demo_users.get(pd['author'])
    category = cat_objects.get(pd['category'])
    if not Post.objects.filter(title=pd['title']).exists():
        post = Post.objects.create(
            title=pd['title'],
            author=author,
            category=category,
            content=pd['content'],
            status='published',
        )
        for tag_name in pd['tags']:
            tag = tag_objects.get(tag_name)
            if tag:
                post.tags.add(tag)
        print(f'  ✓ Post: {pd["title"][:50]}...')

print('\n✅ Demo data seeded successfully!')
print('🌐 Visit http://127.0.0.1:8000/')
print('')
print('👤 ROLES & CREDENTIALS')
print('   Admin  → admin / admin123   (Django admin + all site access)')
print('   Author → alice / alice123   (can write, edit, delete posts)')
print('   Author → bob   / bob123')
print('   Author → carol / carol123')
print('   Reader → reader/ reader123  (can read, comment, like, follow)')
