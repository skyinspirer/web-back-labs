function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i<films.length; i++) {
            let tr = document.createElement('tr');

            let tdTitle = document.createElement('td');
            let tdTitleRus = document.createElement('td');
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');

            tdTitleRus.innerText = films[i].title_ru;
            tdTitle.innerText = films[i].title;
            tdYear.innerText = films[i].year;
            tdTitle.style.fontStyle = 'italic';
            tdTitle.style.color = 'gray';

            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.className = 'btn btn-success';
            editButton.onclick = function() {
                editFilm(films[i].id);
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.className = 'btn btn-danger';
            delButton.onclick = function() {
                deleteFilm(films[i].id, films[i].title_ru);  
            }

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильмов:', error);
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function(response) {
            if(response.ok) {
                fillFilmList();
            } else {
                alert('Ошибка при удалении фильма');
            }
        })
        .catch(function(error) {
            console.error('Ошибка:', error);
            alert('Ошибка при удалении фильма');
        });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (data) {
        return data.json();
    })
    .then(function (film) {
        document.getElementById('id').value = film.id; 
        document.getElementById('title').value = film.title;
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        document.getElementById('description-error').innerText = '';
        
        
        document.getElementById('modal-title').innerText = 'Редактировать фильм';
        showModal();
    })
    .catch(function(error) {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Ошибка при загрузке данных фильма');
    });
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
    document.querySelector('.modal-overlay').style.display = 'block';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
    document.querySelector('.modal-overlay').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description-error').innerText = '';
    
    let titleRuError = document.getElementById('title-ru-error');
    if (titleRuError) titleRuError.innerText = '';
    
    let yearError = document.getElementById('year-error');
    if (yearError) yearError.innerText = '';
    
    document.getElementById('modal-title').innerText = 'Добавить фильм';
    showModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    }

    // ВАЖНОЕ ИСПРАВЛЕНИЕ: URL для POST должен быть без id
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    document.getElementById('description-error').innerText = '';
    
    let titleRuError = document.getElementById('title-ru-error');
    if (titleRuError) titleRuError.innerText = '';
    
    let yearError = document.getElementById('year-error');
    if (yearError) yearError.innerText = '';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
            return null; // Чтобы не переходить к следующему .then
        } else {
            return resp.json();
        }
    })
    .then(function(errors) {
        if(errors) {
            if(errors.description) {
                document.getElementById('description-error').innerText = errors.description;
            }
            if(errors.title_ru) {
                let titleRuError = document.getElementById('title-ru-error');
                if (!titleRuError) {
                    titleRuError = document.createElement('div');
                    titleRuError.id = 'title-ru-error';
                    titleRuError.className = 'error-message';
                    document.getElementById('title-ru').parentNode.appendChild(titleRuError);
                }
                titleRuError.innerText = errors.title_ru;
            }
            if(errors.year) {
                let yearError = document.getElementById('year-error');
                if (!yearError) {
                    yearError = document.createElement('div');
                    yearError.id = 'year-error';
                    yearError.className = 'error-message';
                    document.getElementById('year').parentNode.appendChild(yearError);
                }
                yearError.innerText = errors.year;
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при сохранении фильма');
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});