Changelog
=========

0.0.7 (Current)
---------------

* Course requirements now are presented as an array of objects 
  containing a list "OR" disciplines.
* Courses with no requirements now have a list of empty requirements
  (fixes #35).
* Courses now have a "turmas" attribute corresponding to the current
  term classes (fixes #6).

0.0.6
-----

* "turma" in `/periodos/2016s2/oferecimentos/MC878/turma/a/matriculados`
  changes to its plural form "turmas".
* Parameters pre-processing (including sensitivity) are now declared
  in the views themselves, through the attribute `route_parameters`.

0.0.5
-----

* Started tracking.
