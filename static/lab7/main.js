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
            // Исправлено: создаем замыкание для сохранения значения id
            editButton.addEventListener('click', (function(filmId) {
                return function() {
                    editFilm(filmId);
                };
            })(films[i].id));

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.className = 'btn btn-danger';
            // Исправлено: создаем замыкание для сохранения значений id и title
            delButton.addEventListener('click', (function(filmId, filmTitle) {
                return function() {
                    deleteFilm(filmId, filmTitle);
                };
            })(films[i].id, films[i].title_ru));

            tdActions.append(editButton);
            tdActions.append(delButton);

            tr.append(tdTitleRus);
            tr.append(tdTitle);
            tr.append(tdYear);
            tr.append(tdActions);

            tbody.append(tr);
        }
    });
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function (response) {
            if (response.ok) {
                fillFilmList(); // Обновляем список после удаления
            } else {
                alert('Ошибка при удалении фильма');
            }
        })
        .catch(function (error) {
            alert('Ошибка сети при удалении фильма');
        });
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
    .then(function (response) {
        if (!response.ok) {
            throw new Error('Ошибка загрузки фильма');
        }
        return response.json();
    })
    .then(function (film) {
        document.getElementById('id').value = film.id; 
        document.getElementById('title').value = film.title || '';
        document.getElementById('title-ru').value = film.title_ru;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description || '';
        document.getElementById('description-error').innerText = '';
        
        document.getElementById('modal-title').innerText = 'Редактировать фильм';
        showModal();
    })
    .catch(function (error) {
        alert('Не удалось загрузить данные фильма');
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

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
        } else {
            return resp.json();
        }
    })
    .then(function(errors) {
        if(errors && errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }
    })
    .catch(function(error) {
        alert('Ошибка при сохранении фильма');
    });
}