using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections.Generic;

public class JSONAgentManager : MonoBehaviour
{
    [System.Serializable]
    public class Agent
    {
        public int id;
        public int[] pos;
    }

    [System.Serializable]
    public class AgentData
    {
        public List<Agent> agentes;
    }

    [System.Serializable]
    public class CarAgent
    {
        public GameObject car;
        public int id;
    }

    public CarAgent[] carAgents;
    public Transform[] points;
    public AgentData currentAgentData;

    private void Start()
    {
        StartCoroutine(GetRequest("http://127.0.0.1:8000/run_simulation"));
    }

    public IEnumerator GetRequest(string uri)
    {
        while (true)
        {
            UnityWebRequest uwr = UnityWebRequest.Get(uri);
            yield return uwr.SendWebRequest();

            if (uwr.isNetworkError || uwr.isHttpError)
            {
                Debug.LogError("Error While Sending: " + uwr.error);
            }
            else
            {
                string json = uwr.downloadHandler.text;
                DeserializeJSON(json);
                //debug.LogError
                UpdateAgentPositions();
                Debug.Log("Received JSON: " + json);
            }

            

            yield return new WaitForSeconds(1f); // Espera un segundo antes de la próxima solicitud
        }
    }


    private void DeserializeJSON(string json)
    {
        currentAgentData = JsonUtility.FromJson<AgentData>(json);
    }

    void UpdateAgentPositions()
    {
        if (currentAgentData != null)
        {
            foreach (Agent agente in currentAgentData.agentes)
            {
                CarAgent carAgent = FindCarById(agente.id);
                if (carAgent != null)
                {
                    // Crea un nombre de punto basado en la posición del agente.
                    string pointName = $"{agente.pos[0]},{agente.pos[1]}";

                    // Busca el transform del objeto vacío que tiene ese nombre.
                    Transform pointTransform = GameObject.Find(pointName).transform;

                    if (pointTransform != null)
                    {
                        // Actualiza la posición del coche.
                        carAgent.car.transform.position = pointTransform.position;
                        Debug.Log($"Coche ID: {agente.id} movido al punto: {pointName}");
                    }
                    else
                    {
                        Debug.LogError($"No se encontró un punto con el nombre: {pointName} para el coche ID: {agente.id}");
                    }
                }
            }
        }
    }


    private CarAgent FindCarById(int id)
    {
        foreach (CarAgent carAgent in carAgents)
        {
            if (carAgent.id == id)
            {
                return carAgent;
            }
        }
        return null;
    } 
}