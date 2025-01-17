document.addEventListener('DOMContentLoaded', function() {
    const username = 'Amination1'; // نام کاربری گیت‌هاب شما
    const allProjectsContainer = document.getElementById('allProjects');

    // Fetch public repositories from GitHub
    fetch(`https://api.github.com/users/${username}/repos`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data.forEach(repo => {
                if (repo.private === false) { // Only show public repositories
                    const projectElement = document.createElement('div');
                    projectElement.classList.add('project');
                    projectElement.innerHTML = `
                        <h3><a href="${repo.html_url}" target="_blank">${repo.name}</a></h3>
                        <p>${repo.description || 'توضیحی در دسترس نیست.'}</p>
                    `;
                    allProjectsContainer.appendChild(projectElement);
                }
            });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            allProjectsContainer.innerHTML = '<p>خطا در بارگذاری پروژه‌ها.</p>';
        });
});
