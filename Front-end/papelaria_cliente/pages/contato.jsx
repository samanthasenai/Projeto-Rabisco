import Titulo from '@/components/Titulo';
import Headerb from '../components/Headerb';
import * as React from "react";
import styles from './Contato.module.css'; // Importando o CSS Module

export default function Contato() {
  const [users, setUsers] = React.useState([]);

  const f = async () => {
    const res = await fetch("https://reqres.in/api/users/");
    const json = await res.json();
    setUsers(json.data);
  };

  React.useEffect(() => {
    f();
  }, []);

  return (
    <>
      <Headerb />
      <Titulo texto="Entre em contato conosco!" />
      <div className={styles.App}>
        <div className={styles.flex}>
          {users.length > 0 && 
            users.map((user) => (
              <div key={user.id} className={styles.card}>
                <p>
                  <strong>{user.first_name}</strong>
                </p>
                <p>{user.email}</p>
                <img className={styles.avatar} src={user.avatar} alt={`${user.first_name}'s avatar`} />
              </div>
            ))
          }
        </div>
      </div>
    </>
  );
}
