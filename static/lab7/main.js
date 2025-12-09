function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        for(let i = 0; i < films.length; i++) {
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
            editButton.style.backgroundColor = 'rgba(255, 203, 105, 0.836)';
            editButton.onclick = function() {
                editFilm(films[i].id);  
            };

            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.style.backgroundColor = 'rgb(255, 154, 154)';
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
}

function deleteFilm(id, title) {
    if(! confirm(`Вы точно хотите удалить фильм "${title}"?`))
        return;

    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
        .then(function () {
            fillFilmList();
        })
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
        showModal();
    })
}
function showModal() {
    document.querySelector('div.modal').style.display = 'block'; 

    document.getElementById('description-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
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
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
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

    const url = `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';


    document.getElementById('description-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';

    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(film)
    })
    .then(function(resp) {
        if(resp.ok) {
            fillFilmList();
            hideModal();
        }
        return resp.json();
    })
    .then(function(errors) {
        if(errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }
        if(errors.title_ru) {
            let titleRuError = document.getElementById('title-ru-error');
            if (!titleRuError) {
                titleRuError = document.createElement('div');
                titleRuError.id = 'title-ru-error';
                titleRuError.className = 'error-message';
                document.getElementById('title-ru').appendChild(titleRuError);
            }
            titleRuError.innerText = errors.title_ru;
        }
        if(errors.year) {
            let yearError = document.getElementById('year-error');
            if (!yearError) {
                yearError = document.createElement('div');
                yearError.id = 'year-error';
                yearError.className = 'error-message';
                document.getElementById('year').appendChild(yearError);
            }
            yearError.innerText = errors.year;
        }
    });
}