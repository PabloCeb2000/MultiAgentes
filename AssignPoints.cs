using UnityEngine;

public class AssignPoints : MonoBehaviour
{
    public JSONAgentManager agentManager; // Referencia a tu script JSONAgentManager
    public Transform pointsParent; // Objeto padre que contiene todos los puntos

    void Awake()
    {
        // Asegúrate de que ambos campos estén asignados en el inspector
        if (agentManager != null && pointsParent != null)
        {
            int childCount = pointsParent.childCount;
            agentManager.points = new Transform[childCount];
            for (int i = 0; i < childCount; i++)
            {
                agentManager.points[i] = pointsParent.GetChild(i);
            }
        }
    }
}
