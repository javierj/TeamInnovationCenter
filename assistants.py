
class FactorAnalysisAssistant(object):

    def _all_over(self, values, limit):
        for v in values:
            if v <= limit:
                return False
        return True

    def _all_under(self, values, limit):
        for v in values:
            if v >= limit:
                return False
        return True

    def stats_analysis_2(self, mean, mad):
        """


        mad >= 1
        Los resultados de las enesutas son muy heterogeneas.

        mad < 1
        Los reusltados son consistentes.

        med >= 4
        Buenos reusltados. mantener

        med < 3
        Malos reusltados, ncorregis

        3 <= med < 4
        Resultados correctos, mejorar.
        """
        pass

    def stats_analysis(self, mean, mad):
        """

        mad >= 1
        Los resultados de las enesutas son muy heterogeneas.

        mad < 1
        Los reusltados son consistentes.

        med >= 4
        Buenos reusltados. mantener

        med < 3
        Malos reusltados, ncorregis

        3 <= med < 4
        Resultados correctos, mejorar.

        :param mean:
        :param mad:
        :return:
        """
        if self._all_over(mad, 1):
            if self._all_over(mean, 2.9):
                return "La media y la desviación indica que, aunque la mayoría del equipo tiene una buena opinión, " \
                       "hay una minoría de personas disconformes. Recomendamos conversaciones uno a uno para identificar " \
                       "a las personas con las valoraciones más bajas y conocer cuáles son sus motivos para " \
                       "solucionarlos."
            if self._all_under(mean, 2.1):
                return "La media y la desviación indica que, aunque la mayoría del equipo se muestra disconforme, " \
                       "hay un pequeño número de personas que están contentas. Recomendamos alguna actividad de grupo " \
                       "dónde estas personas puedan compartir sus visiones y se planteen soluciones que cuenten con el " \
                       "consenso de todos, para intentar aumentar el número de personas con una valoración positiva."
            return "Los resultados son demasiado variables para poder extraer una conclusión. Recomendamos realizar " \
                   "actividades de equipo para marcar objetivos comunes y volver a repetir las encuestas para ver su " \
                   "progresión."
        if self._all_under(mad, 1):
            if self._all_over(mean, 2.5):
                return "La media indica que la mayoría de las respuestas están en los valores superiores. " \
                       "Continuad trabajando de esta manera."
            if  self._all_under(mean, 2.5):
                return "La media indica que la mayoría de las repsuestas están en los valores inferiores. Recomendamos organizar alguna actividad grupal que ayude a abordar los problemas y plantear soluciones que mejoren la valoración del equipo."
            return "El equipo está en un nivel intermedio, ni bien ni mal. Puedes aprovechar este estado para mejorar otro factor que esté por detrás o seguir trabajando en actividades para potenciar este factor."
        # Never reached.
        return "Las desviaciones indican que las preguntas de un mismo factor no son consistentes. Se recomienda repetir la encuesta en unas semanas."
