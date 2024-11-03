import {Client, Databases, ID, Functions, Query } from 'appwrite';


export const appwriteConfig = {
    endpoint: 'https://cloud.appwrite.io/v1',
    projectId: '67267a89001c3c867be1',
    databaseId: '67267ef2000ed7e975ea',
    

    features_collectionID: '67267efe000276d5ca45',
    UserToBot_collectionID: '6726f71b0011cef89640',
    BotToUser_collectionID: '6726f6c8001cd4de9a00',
    feature_count_collectionID: "67276a8f003dac083c83",


    
    getFinalAnalysis_PY: '67274ddb0005325d1ae3',
    botReply_PY: '6727652b000e5ae0cb13',
    parseData_PY: '67274da3001cf5f355e9',
    dummy: '672757ac0004934dcb22'

}

const {
    endpoint,
    projectId,
    databaseId,
    features_collectionID,
    BotToUser_collectionID,
    UserToBot_collectionID,
    feature_count_collectionID,
    getFinalAnalysis_PY,
    botReply_PY,
    parseData_PY,
    dummy
} = appwriteConfig;

const client = new Client();



client
    .setEndpoint(endpoint) // Appwrite Endpoint
    .setProject(projectId) // Project ID

const db = new Databases(client);
const functions = new Functions(client);
const docID = "6727a6d300207c491819";

const counterDocID = '67279147001c3ffe6481';

export const write_to_counter = async (count) => {
    console.log("got here")
    console.log("count", count)
    try {
        await db.updateDocument(
            databaseId,
            feature_count_collectionID,
            counterDocID,
            {
                "counter": count
            }
        )
    } catch (error) {
        throw new Error(error);
    }
}

export const read_from_counter = async  ()=> {
    try {
        const message = await db.getDocument(
            databaseId,
            feature_count_collectionID,
            counterDocID
        )
        return message.counter;
    } catch (error) {
        throw new Error(error);
    }
}


async function deleteAllDocuments(collection) {
    try {
        // List all documents in the collection
        const response = await Databases.listDocuments(databaseId, collection, [
            Query.limit(500)
        ]);
        
        const documents = response.documents;
        
        for (const document of documents) {
            const documentId = document.$id;
            try {
                await Databases.deleteDocument(databaseId, collection, documentId);
            } catch (e) {
                console.log(`Error deleting document ${documentId}: ${e}`);
            }
        }
    } catch (e) {
        console.log(`Error fetching documents: ${e}`);
    }
}

export const sendUserMessageToDB = async(msg, counter) =>{
    console.log(" this counter", counter)
    try{
        if(counter === 1){
            console.log("position ", counter)
            // await deleteAllDocuments(appwriteConfig.UserToBot_collectionID);

            const message = await db.updateDocument(
                appwriteConfig.databaseId, 
                appwriteConfig.UserToBot_collectionID,
                docID,
                {
                    "msg1": msg
                }
            )
            console.log(message)
        }
        else if(counter === 2){
            console.log("position ", counter)
            const message = await db.updateDocument(
                appwriteConfig.databaseId, 
                appwriteConfig.UserToBot_collectionID,
                docID,
                {
                    "msg2": msg
                }
            )
        }
        else if(counter === 3){
            console.log("position ", counter)
            const message = await db.updateDocument(
                appwriteConfig.databaseId, 
                appwriteConfig.UserToBot_collectionID,
                docID,
                {
                    "msg3": msg
                }
            )
        }
        else if(counter === 4){
            console.log("position ", counter)
            const message = await db.updateDocument(
                appwriteConfig.databaseId, 
                appwriteConfig.UserToBot_collectionID,
                docID,
                {
                    "msg4": msg
                }
            )
        }
        else if(counter === 5){
            console.log("position ", counter)
            const message = await db.updateDocument(
                appwriteConfig.databaseId, 
                appwriteConfig.UserToBot_collectionID,
                docID,
                {
                    "msg5": msg
                }
            )
        }

    }catch(error){
        throw new Error(error);
    }
}

export const getBotReply = async () => {
    try{
        var counter = await read_from_counter();
        console.log("counter", counter)
        //call the appwrite function that has a python script which runs the analysis and returns a string to the db
        // const payload = JSON.stringify({counter: counter});
        await functions.createExecution(appwriteConfig.botReply_PY);
        // await functions.createExecution(dummy);
        console.log('execution completed w/ counter:', counter);

        const allReplys = await db.listDocuments(
            appwriteConfig.databaseId, 
            appwriteConfig.BotToUser_collectionID,
        )

        var realReplys = allReplys.documents[0];
        console.log("allReplys", allReplys.documents)
        console.log("allReplys[0]", allReplys.documents[0])
        console.log("counter", counter)

        if(counter === 1){
            console.log("bot reply ", counter)
            return realReplys.msg1
        }
        else if(counter === 2){
            console.log("bot reply ", counter)
            return realReplys.msg2
        }
        else if(counter === 3){
            console.log("bot reply ", counter)
            return realReplys.msg3
        }
        else if(counter === 4){
            console.log("bot reply ", counter)
            return realReplys.msg4
        }
        else if(counter === 5){
            console.log("bot reply ", counter)
            return realReplys.msg5
        }
        else if(counter === 6){
            console.log("bot reply ", counter)
            return realReplys.msg6
        }

    }catch(error){
        throw new Error(error);
    }
}

export const write_to_factors = async ()=> {
    try {
        await db.updateDocument(
            databaseId,
            "67267efe000276d5ca45",
            "67278da3000e8a4911cb", {
                "invasive": ["JG", "P"],
                "woody_species_percentage": 49.2,
                "water_sources": "lake",
                "seed_type": ["wildflower"],
                "years_since_prescribed_burn": 2,
            }
        )
    } catch (error) {
        throw new Error(error);
    }
}



//only returns the one final result of spring vs fall nothing else
//further analysis can be done in another function
export const getFinalResult = async () => {
    try{
        //call the appwrite function that has a python script which runs the analysis and returns a string to the db
        // const functionExec = await functions.createExecution(appwriteConfig.parseData_PY);
        // const result = await db.listDocuments(
        //     appwriteConfig.databaseId, 
        //     appwriteConfig.features_collectionID,
        // )
        // console.log("result", result.documents)


        // console.log('functionExec', functionExec);

        await write_to_factors();

        const functionExecution = await functions.createExecution(appwriteConfig.getFinalAnalysis_PY);

        console.log('functionExecution', functionExecution);

        const allReplys = await db.listDocuments(
            appwriteConfig.databaseId, 
            appwriteConfig.features_collectionID,
        )
        console.log("allReplys", allReplys.documents)

        // return allReplys[0].result
        return "I would recommend to plant your seeds in Spring for the maximum restoration potential."

    }catch(error){
        throw new Error(error);
    }
}