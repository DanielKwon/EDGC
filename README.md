# MeshParser

     ============= MeshParser v1.0 =================
    | Find the disease name for input keyword      |
    | - input keyword can be name or uniqueid      |
     ===============================================

    Usage : python MeshParser.py MeSH(xml) keyword direction result_type
            * keyword     : category or disease name in MeSH / whole / whole-path
            * direction   : up(categories) / down(dieseases)
            * result_type : all / unique (for direction down only)

Required : MeSH(xml) should be downloaded to your machine before use
          ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/xmlmesh/desc2017.xml
          
          
Example :

      1. To Find a tree structure for given keyword(disease name or unique id)
         : python MeshParser.py desc2017.xml Hemianopsia up all
         
         (Nervous System Diseases : D009422) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Vision Disorders : D014786) >  [Hemianopsia : D006423]
        (Eye Diseases : D005128) >  (Vision Disorders : D014786) >  (Blindness : D001766) >  [Hemianopsia : D006423]
        (Pathological Conditions, Signs and Symptoms : D013568) >  (Signs and Symptoms : D012816) >  (Neurologic Manifestations : D009461) >  (Sensation Disorders : D012678) >  (Vision Disorders : D014786) >  [Hemianopsia : D006423]

         : python MeshParser.py desc2017.xml D006423 up all
           same result as above
           
      2. To find a disease name for some category (name or unique id)
         : python MeshParser.py desc2017.xml "Sensation Disorders" down all
         
          Olfaction Disorders (D000857)
          Hyperesthesia (D006941)
          Paresthesia (D010292)
          Hypesthesia (D006987)
          Hyperalgesia (D006930)
          Dysgeusia (D004408)
          Ageusia (D000370)
          Diplopia (D004172)
          Amblyopia (D000550)
          ...
      
         : python MeshParser.py desc2017.xml "Sensation Disorders" down unique
          same result as above but no duplilcated disease name
          
       3. To find whole tree for MeSH
         : python MeshParser.py desc2017.xml whole-path down all
         
         result is on github
