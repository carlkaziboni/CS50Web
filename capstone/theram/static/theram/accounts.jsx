import axios from "axios";
import { createRoot } from "react-dom/client";

var tbody = null

document.addEventListener("DOMContentLoaded", async () =>
    {
        let table = await Tablefunc();
        tbody = createRoot(document.getElementById("tbody"));
        tbody.render(table);
    }
    );

function reset_user(username) {
    const csrftoken = getCookie('csrftoken');
    axios.post("/api/accounts",{
        username: username},{
            headers:{
                'X-CSRFToken': csrftoken
            }
        }).then(function (response){
        alert(response.data['message']);
    });
};

function delete_user(username){
    const csrftoken = getCookie('csrftoken');
    axios.delete("/api/accounts/" + username, {
        headers:{
            'X-CSRFToken': csrftoken
        }
    }).then(async function (response){
        alert(response.data['message']);
        let table = await Tablefunc();
        //let tbody = createRoot(document.getElementById("tbody"));
        tbody.render(table);
    });
};

async function Tablefunc() {
    let user_list = null;
    let response = await axios.get("/api/accounts");
    let users = response.data;
        user_list = users.map(user => 
            <tr key={user['username']}>
                <td>{user['username']}</td>
                <td>
                    <button onClick={() => reset_user(user['username'])} className="btn btn-primary">Reset</button>
                </td>
                <td>
                    <button onClick={() => delete_user(user['username'])} className="btn btn-primary">Delete</button>
                </td>
            </tr>
        );
    return user_list;
  }


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}