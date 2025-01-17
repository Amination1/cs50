document.addEventListener('DOMContentLoaded', function() {
    const username = 'Amination1'; // نام کاربری گیت‌هاب شما
    const profileInfoContainer = document.getElementById('profileInfo');
    const projectsContainer = document.getElementById('projects');
    const languagesContainer = document.getElementById('languages');
    const readmeContentContainer = document.getElementById('readmeContent'); // Element for README content

    // Map of languages and tools to their corresponding icons
    const languageIcons = {
        'PHP': 'https://img.icons8.com/color/48/000000/php.png',
        'Laravel': 'https://img.icons8.com/color/48/000000/laravel.png',
        'JavaScript': 'https://img.icons8.com/color/48/000000/javascript.png',
        'HTML': 'https://img.icons8.com/color/48/000000/html-5.png',
        'CSS': 'https://img.icons8.com/color/48/000000/css3.png',
        'Python': 'https://img.icons8.com/color/48/000000/python.png',
        'C': 'https://img.icons8.com/color/48/000000/c-plus-plus-logo.png',
        'NestJS': 'https://img.icons8.com/color/48/000000/nestjs.png',
        'Git': 'https://img.icons8.com/color/48/000000/git.png',
        'Django': 'https://img.icons8.com/color/48/000000/django.png',
    };

    // Fetch profile information from GitHub
    fetch(`https://api.github.com/users/${username}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display profile information
            profileInfoContainer.innerHTML = `
                <img src="${data.avatar_url}" alt="${data.login}" class="avatar">
                <h3>${data.name || data.login}</h3>
                <p>${data.bio || 'توضیحی در دسترس نیست.'}</p>
                <p>تعداد دنبال‌کنندگان: ${data.followers}</p>
                <p>تعداد دنبال‌شده‌ها: ${data.following}</p>
            `;
            // Fetch README file
            fetch(`https://raw.githubusercontent.com/${username}/${username}/main/README.md`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(readme => {
                    readmeContentContainer.innerHTML = `<div>${readme}</div>`;
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation for README:', error);
                    readmeContentContainer.innerHTML = '<p>خطا در بارگذاری فایل README.</p>';
                });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            profileInfoContainer.innerHTML = '<p>خطا در بارگذاری اطلاعات پروفایل.</p>';
        });

    // Fetch public repositories from GitHub
    fetch(`https://api.github.com/users/${username}/repos`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Sort repositories by updated_at date and display the latest 5
            const latestProjects = data.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at)).slice(0, 5);
            latestProjects.forEach(repo => {
                if (repo.private === false) { // Only show public repositories
                    const projectElement = document.createElement('div');
                    projectElement.classList.add('project');
                    projectElement.innerHTML = `
                        <h3><a href="${repo.html_url}" target="_blank">${repo.name}</a></h3>
                        <p>${repo.description || 'توضیحی در دسترس نیست.'}</p>
                    `;
                    projectsContainer.appendChild(projectElement);
                }
            });

            // Display language and tool icons
            const languages = new Set();
            data.forEach(repo => {
                if (repo.language) {
                    languages.add(repo.language); // Add language to the set
                }
            });
            languagesContainer.innerHTML = Array.from(languages).map(lang => {
                const iconUrl = languageIcons[lang];
                return iconUrl ? `<img src="${iconUrl}" alt="${lang}" class="language-icon">` : '';
            }).join('') || 'توضیحی در دسترس نیست.';
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            projectsContainer.innerHTML = '<p>خطا در بارگذاری پروژه‌ها.</p>';
        });
});
