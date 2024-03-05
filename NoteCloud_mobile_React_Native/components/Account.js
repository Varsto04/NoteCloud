import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, Button, Platform, ScrollView, BackHandler, TouchableOpacity, Image, Linking, SafeAreaView, } from 'react-native';
import axios from 'axios';

import * as SQLite from 'expo-sqlite';
import { useState, useEffect,} from 'react';
import CryptoJS from 'crypto-js';


export default function Account({ navigation }) {
  const [inputLogin, setInputLogin] = useState('');
  const [inputPassword, setInputPassword] = useState('');
  const [token, setToken] = useState('');
  const [login, setLogin] = useState();
  const [user_id, setUser_id] = useState();
  const [notes, setNotes] = useState([]);
  const [db, setDb] = useState(SQLite.openDatabase('example.db'));
  const [isLoading, setIsLoading] = useState(true);


  const update = () => {db.transaction(tx => {
    tx.executeSql('SELECT * FROM logins', null,
      (txObj, resultSet) => console.log(resultSet.rows._array), //(txObj, resultSet) => setLogins(resultSet.rows._array),      console.log(resultSet.rows._array)
      (txObj, error) => console.log(error)
    );
  });};

  const update_notes = () => {db.transaction(tx => {
    tx.executeSql('SELECT * FROM notes ',null,
      (txObj, resultSet) => (setNotes(resultSet.rows._array)),
      (txObj, error) => console.log(error)
    );
  });};
  
  // FIX THIS!!!
  const showLogins = () => {
    // CONSOLE LOG
    // {update()}
    {update_notes()}
    {select_login()}
    };
        
  
  // CLOUD      
  const updateLogin = (login,jwt_token,user_id) => {
    db.transaction(tx => {
      tx.executeSql('UPDATE logins SET login =?,jwt_token=?,user_id=?  where id=1 ', [login,jwt_token,user_id]
      );
    });
    db.transaction(tx => {
      tx.executeSql('SELECT * FROM logins', null,
        (txObj, resultSet) => console.log(resultSet.rows._array),
        (txObj, error) => console.log(error)
      );
    });
  };


  useEffect(() => {
    fetch('http://192.168.45.14:8000/mobile/get_csrf_token', { 
      method: 'GET', 
      credentials: 'include'  
    }) 
    .then(response => response.json()) 
    .then(data => { 
      setToken(data.csrf_token);
    }); 
  }, []); 
  

  const sendLoginToServer = () => {
    if (inputLogin=='admin' && inputPassword =='admin'){updateLogin('admin','-1','-1'),navigation.navigate('Main')}
    else if (inputLogin=='online_admin' && inputPassword =='online_admin'){updateLogin('online_admin','-1','-2'),navigation.navigate('Main')}
    else{
    fetch('http://192.168.45.14:8000/mobile/get_salt', { 
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json', 
        'X-CSRFToken': token
      }, 
      credentials: 'include',
      body: JSON.stringify({ 'login': (inputLogin)})
    }) 
    .then(response => response.json()) 
    .then(data => {sendPasswordToServer(data.salt)})
  }
  };


  const sendPasswordToServer = (salt) => { 
    fetch('http://192.168.45.14:8000/mobile/mobile_login', { 
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json', 
        'X-CSRFToken': token
      }, 
      credentials: 'include',
      body: JSON.stringify({ 'login': (inputLogin),'password': (CryptoJS.PBKDF2(inputPassword, salt, { keySize: 256/32, iterations: 50000 }).toString(CryptoJS.enc.Base64))}
      ) 
    }) 
    .then(response => response.json()) 
    .then(data => {if (data.message) {updateLogin(inputLogin,data.jwt_token,data.id_user), get_data()} //.then(data => {updateLogin(inputLogin,data.jwt_token)
      // Handle response
    }); 
  }; 
  // CLOUD


  // CLOUD
  const get_data = () => {
    db.transaction(tx => {
    tx.executeSql('SELECT login,jwt_token FROM logins', null,
      (txObj, resultSet) => (get_csrf_token(resultSet.rows._array[0].login,resultSet.rows._array[0].jwt_token)),
      (txObj, error) => console.log(error));
    });
  };


  const get_csrf_token = (login, jwt_token) => {
    fetch('http://192.168.45.14:8000/mobile/get_csrf_token', { 
      method: 'GET', 
      credentials: 'include'  
    }) 
    .then(response => response.json()) 
    .then(data => {sendUpdateToServer(data.csrf_token, login, jwt_token);
    });
  };

  const sendUpdateToServer = (token, login, jwt_token) => {
    fetch('http://192.168.45.14:8000/mobile/get_data', { 
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json', 
        'X-CSRFToken': token
      }, 
      credentials: 'include',
      body: JSON.stringify({'login':login, 'jwt_token':jwt_token})
    }) 
    .then(response => response.json()) 
    .then(data => {contains(data.data), console.log('recieve notes')}) //contains(notes,data.data) insert_data(data.data)
  };



  function contains(data) {
    let xer = [];
    let xer_part = [];

    notes.forEach((notes_part) => {
      xer_part.push(notes_part['note']);
      xer_part.push(notes_part['user_id']);
      xer_part.push(notes_part['id']);
      xer.push(xer_part);
      xer_part = [];
    });
    // log xer
    // console.log(xer);

    data.forEach((data_part) => {
      let flag = false;
      let id_note = -2;

      xer.forEach((xer_part2) => {
        if (xer_part2[0] === data_part[2] && xer_part2[1] === data_part[1]) {
          flag = true;
          id_note = xer_part2[2];
        }
      });

    if (!flag && id_note === -2) {
      insert_data(data_part);
    } else if (flag && id_note !== -2) {
      updateContent(data_part,id_note);
    }
  });
  }

  const addNote = (user_id,title,content,user1_id,content_user1,user2_id,content_user2,user3_id,content_user3) => {
    let count = 0;
    for (let i = 0; i < notes.length; i++) {
      console.log(notes[i].note)
      if (notes[i].note === title && notes[i].id === user_id) {
        count++;
      }
    }
    console.log(count);
    if (count === 0) {
      db.transaction(tx => {
      tx.executeSql('INSERT INTO notes (editable,user_id,note,content,user1_id,content_user1,user2_id,content_user2,user3_id,content_user3)values(?,?,?,?,?,?,?,?,?,?)', [0,user_id,title,content,user1_id,content_user1,user2_id,content_user2,user3_id,content_user3],
                  // user_id note content editable user1_id content_user1 user2_id content_user2 user3_id content_user3
      (txObj, resultSet) => {
          let existingNotes = [...notes];
          existingNotes.push({ id: resultSet.insertId, note: title});
          setNotes(existingNotes);
        },

        (txObj, error) => console.log(error)
      );
      });
    } else {console.log('already exist')}
  }

  const insert_data = (data) => {
    addNote(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]),navigation.navigate('Main')
  };

  const updateContent = (data,id_note) => {
    db.transaction(tx => {
      tx.executeSql('UPDATE notes SET editable=?,user_id=?,note=?,content=?,user1_id=?,content_user1=?,user2_id=?,content_user2=?,user3_id=?,content_user3=? WHERE id=?',
      [0,data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],id_note]
      );
    });
    navigation.navigate('Main')
  };
  //CLOUD

  
  const select_login = () => {
    db.transaction(tx => {
    tx.executeSql('SELECT login,jwt_token,user_id FROM logins', null,
      (txObj, resultSet) => (setLogin(resultSet.rows._array[0].login), setUser_id(resultSet.rows._array[0].user_id), setIsLoading(false)),
      (txObj, error) => console.log(error));
    });
  };

  const delete_notes = () =>{
    console.log('notes deleted')
    db.transaction(tx => {
      tx.executeSql('DELETE FROM notes WHERE user_id != -1', null,);
      });
  }

// MAIN RETURN
  if (isLoading){
    return (
      <View style={styles.loading}>
        <Text>Loading...</Text>
        {select_login()}
      </View>
    );}

  else if (login==''){return (
    
    <SafeAreaView style={styles.container}>
      <StatusBar animated = {true} hidden = {true} />
      {showLogins()}
      <Image source={require('../assets/logo.png')} style={{width:171*1.75, height:30*1.75, margin:8}}/>
      
      <View style={styles.container}>
      <TextInput style={{fontSize: 30}} value={inputLogin} onChangeText={setInputLogin} placeholder={'Login'}/> 
      <TextInput style={{fontSize: 30}} value={inputPassword} onChangeText={setInputPassword} placeholder={'Password'} secureTextEntry={true}/>
      <TouchableOpacity style={{fontSize: 20, marginTop: 10,borderWidth: 1,paddingVertical: 10,paddingHorizontal: 30,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
      onPress={()=>{sendLoginToServer(), select_login()}}>
      <Text style={{color:'#fff'}}>Log in</Text>
      </TouchableOpacity>
      </View>
      
      <View style={styles.container}>
      <Text style={styles.textdown} >Don`t have an account?</Text>
      <TouchableOpacity>
        <Text style={{fontSize: 20, color: '#d0b6e5'}} onPress={() => {Linking.openURL("http://192.168.45.14:8000/user/registration").catch(err => {console.error("Failed opening page because: ", err), alert('Failed to open page')})}}>Register</Text>
      </TouchableOpacity>
      </View>

    </SafeAreaView>
  );}

  else if (login!=undefined){return (
    <SafeAreaView style={styles.container}>
      {showLogins()}
      <StatusBar animated = {true} hidden = {true} />
      <Image source={require('../assets/logo.png')} style={{width:171*1.75, height:30*1.75, margin:8}}/>
      <Image source={require('../assets/user.png')} style={{height:90,
    width:90,
    marginTop: 50}}/>
      <View style={styles.container}>
        <Text style={styles.textup}>{login}</Text>
        <Text style={styles.textdown}>{user_id}</Text>
      </View>

      <View style={styles.container}>
      <TouchableOpacity style={{fontSize: 20, marginTop: 10,borderWidth: 1,paddingVertical: 10,paddingHorizontal: 30,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
      onPress={()=>{delete_notes(),updateLogin('','','-1'), select_login()}}>
      <Text style={{color:'#fff'}}>Log out</Text>
      </TouchableOpacity>
      </View>
      <View style={styles.container}><Text></Text></View>
    </SafeAreaView>
  );}

  else{return(
  <SafeAreaView style={styles.container}>
    {showLogins()}
    <StatusBar animated = {true} hidden = {true} />
    <Image source={require('../assets/logo.png')} style={{width:171, height:30, margin:8}}/>
    <TouchableOpacity 
    onPress={()=>{updateLogin('','',''), select_login()}}>
      <Text style={styles.textup}>Welcome to NoteCloud</Text>
      <Text style={styles.textdown}>Here is the account page where You can login and share Notes from Cloud</Text>
    </TouchableOpacity>
  </SafeAreaView>
  );}
};



// STYLES
const styles = StyleSheet.create({
  
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 8
  },


  loading: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },

  row: {
    flexDirection: 'row',
    alignSelf: 'stretch',
    justifyContent: 'space-between',
    margin: 4,
    padding: 8,
  },

  
  textup: {
    fontSize: 30,
  },

  textdown: {
    fontSize: 20,
    
  },

  square_button: {
    height:30,
    width:30,
    margin: 8
  }

});
