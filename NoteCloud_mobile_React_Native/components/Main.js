import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, Button, Platform, ScrollView, TouchableOpacity, Image, SafeAreaView} from 'react-native';

import * as SQLite from 'expo-sqlite';
import { useState, useEffect } from 'react';
import { get } from 'react-native/Libraries/Utilities/PixelRatio';
import axios from 'axios';
import { useIsFocused } from '@react-navigation/native';

export default function Main({ navigation }) {
  const [db, setDb] = useState(SQLite.openDatabase('example.db'));
  const [isLoading, setIsLoading] = useState(true);
  const [notes, setNotes] = useState([]);
  const [currentNote, setCurrentNote] = useState(undefined);

 // I DELETE UPDATE IN FIRST USEEFFECT EVERYWHERE
  useEffect(() => {

    // db.transaction(
    //   tx => {
    //     tx.executeSql('drop table logins')
    //   }
    // );

    // db.transaction(
    //   tx => {
    //     tx.executeSql('update notes set user1_id = null where editable = 1')
    //   }
    // );
    
    db.transaction(tx => {
      tx.executeSql('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, note TEXT, content TEXT, editable INTEGER, user1_id INTEGER, content_user1 TEXT, user2_id INTEGER, content_user2 TEXT, user3_id INTEGER, content_user3 TEXT)')
    });

  
    db.transaction(tx => {
      tx.executeSql('CREATE TABLE IF NOT EXISTS logins (id INTEGER PRIMARY KEY, login TEXT, jwt_token TEXT, user_id INTEGER);')
    });

    db.transaction(tx => {
      tx.executeSql('INSERT INTO logins (id, jwt_token, login, user_id) values (1,null,null,null);')
    });

    setIsLoading(false);
    
  }, [db]);

  if (isLoading) {
    return (
      <View style={styles.loading}>
        <Text>Loading notes...</Text>
      </View>
    );
  }


// MAIN PART
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
          setCurrentNote(undefined);
        },

        (txObj, error) => console.log(error)
      );
      });
    } else {console.log('already exist')}
  }
    


  const deleteNote = (id) => {
    db.transaction(tx => {
      tx.executeSql('DELETE FROM notes WHERE id = ?', [id],
        
      (txObj, resultSet) => {
          if (resultSet.rowsAffected > 0) {
            let existingNotes = [...notes].filter(note => note.id !== id);
            setNotes(existingNotes);
          }
        },

        (txObj, error) => console.log(error)
      );
    });
  };

  // const select_id = () => {
  //   db.transaction(tx => {
  //   tx.executeSql('SELECT * FROM logins', null,
  //     (txObj, resultSet) => (update(resultSet.rows._array[0].user_id)),
  //     (txObj, error) => console.log(error));
  //   });
  // };

  const update = () => {db.transaction(tx => {
    tx.executeSql('SELECT * FROM notes ',null,
      (txObj, resultSet) => (setNotes(resultSet.rows._array)),
      (txObj, error) => console.log(error)
    );
  });};


  const edit = (id) => {
    db.transaction(tx => {

      tx.executeSql("UPDATE notes SET editable = 0")
      tx.executeSql('UPDATE notes SET editable = ? WHERE id = ?', [1, id])});
    
    navigation.navigate('WorkPlace')};
  
  
  const select_login = () => {
    db.transaction(tx => {
    tx.executeSql('SELECT * FROM logins', null,
      (txObj, resultSet) => (addNote(resultSet.rows._array[0].user_id,currentNote)),
      (txObj, error) => console.log(error));
    });
  };


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
    .then(data => {contains(data.data)}) //contains(notes,data.data) insert_data(data.data)
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


  const insert_data = (data) => {
    addNote(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])
  };

  const updateContent = (data,id_note) => {
    db.transaction(tx => {
      tx.executeSql('UPDATE notes SET editable=?,user_id=?,note=?,content=?,user1_id=?,content_user1=?,user2_id=?,content_user2=?,user3_id=?,content_user3=? WHERE id=?',
      [0,data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],id_note]
      );
    });
  };
  //CLOUD

  
  // RETURN  
  const showNotes = () => {
    // FIXED
    {update()}
    
    return notes.map((note, index) => {
      // OFFLINE NOTES
      if (note.user_id == -1){return (
        <View key={index} style={{flexDirection: 'row',
        // alignItems: 'center',
        alignSelf: 'stretch',
        justifyContent: 'space-between',
        margin: 8,
        marginBottom:20}}>
          <TouchableOpacity style={styles.container} onPress={() => edit(note.id)}>
            <Text style={styles.text_up}>📌{note.note}</Text>
            <Text numberOfLines={2} style={styles.text_down}>📋{note.content}</Text>
          </TouchableOpacity>

          <TouchableOpacity style={{borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
          onPress={() => deleteNote(note.id)}>
            <Image source={require('../assets/trash.png')} style={styles.square_button}/>
          </TouchableOpacity>
        </View>
      );}
      // ONLINE NOTES
      else{return (
        <View key={index} style={{flexDirection: 'row',
        // alignItems: 'center',
        alignSelf: 'stretch',
        justifyContent: 'space-between',
        margin: 8,
        marginBottom:20
        }}>
          <TouchableOpacity style={styles.container} onPress={() => edit(note.id)}>
            
            <Text style={styles.text_up}>📌{note.note}</Text>
            <Text style={{color:'#8a7998',fontSize:20}}>☁️{note.user_id} {note.user1_id} {note.user2_id} {note.user3_id}</Text>
            <Text numberOfLines={2} style={styles.text_down}>📋{note.content}</Text>
          </TouchableOpacity>
          
          <TouchableOpacity onPress={() => deleteNote(note.id)}>
            <View style={{borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000}}>
            <Image source={require('../assets/trash.png')} style={styles.square_button}/>
            </View>
          </TouchableOpacity>
        </View>
      );}
    });
  };
  

// MAIN RETURN
  return (
    <SafeAreaView style={styles.container}>
      
      <StatusBar animated = {true} hidden = {true} />

      <View style={styles.row}>
      <TouchableOpacity onPress={()=>navigation.navigate('Account') }>
        <Image source={require('../assets/user.png')} style={styles.square_button}/>
      </TouchableOpacity>
      
      <TouchableOpacity activeOpacity={1} delayLongPress={2500} onLongPress={()=>{console.log("LogoPressed")}}>
      <Image source={require('../assets/logo.png')} style={{width:171, height:30, margin:8}}/>
      </TouchableOpacity>
      
      <TouchableOpacity onPress={get_data}>
        <Image source={require('../assets/cloud.png')} style={styles.square_button}/>
      </TouchableOpacity>
      </View>

      <View style={styles.row}>
        <TextInput style={styles.text_up} maxLength={20} editable value={currentNote} defaultValue='' placeholder='note' onChangeText={setCurrentNote} />
        {(currentNote != undefined && currentNote != '')?
        <TouchableOpacity style={{borderWidth: 1,paddingVertical: 5,paddingHorizontal: 5,borderColor: '#fff',backgroundColor: '#d0b6e5',borderRadius: 1000,textAlign: 'center'}}
        onPress={select_login}> 
          <Image source={require('../assets/add.png')} style={styles.square_button}/>
        </TouchableOpacity>:null}
        {/* <Button title='show notes' onPress={()=>{console.log(notes)}}/> */}
      </View>


      <ScrollView style={styles.container}>
        {showNotes()}
      </ScrollView>
      
    
    </SafeAreaView>
  );  
}



// STYLES
const styles = StyleSheet.create({
  
  container: {
    flex: 1,
    backgroundColor: '#fff',
    // alignItems: 'center',
    // justifyContent: 'center',
  },

  loading: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  
  row: {
    flexDirection: 'row',
    // alignItems: 'center',
    alignSelf: 'stretch',
    justifyContent: 'space-between',
    margin: 8
  },


  text_up: {
    flex: 0.9,
    fontSize: 30,
  },

  text_down: {
    flex: 0.9,
    fontSize: 20,
  },

  square_button: {
    height:30,
    width:30,
    margin: 8
  }
});
