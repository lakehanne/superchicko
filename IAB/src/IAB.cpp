#include <sstream>
using std::ostringstream ;
#include <fstream>

#include <string>
using std::string;

#include <vector>
using std::vector;

//#include <IAB/IAB-config.h>
#include <sofa/helper/ArgumentParser.h>
#include <SofaSimulationCommon/common.h>
#include <sofa/simulation/Node.h>
#include <sofa/helper/system/PluginManager.h>
#include <sofa/simulation/config.h> // #defines SOFA_HAVE_DAG (or not)
#include <SofaSimulationCommon/init.h>
#ifdef SOFA_HAVE_DAG
#include <SofaSimulationGraph/init.h>
#include <SofaSimulationGraph/DAGSimulation.h>
#endif

using sofa::simulation::Node;
#include <sofa/simulation/SceneLoaderFactory.h>
#include <SofaGraphComponent/SceneCheckerListener.h>
using sofa::simulation::scenechecking::SceneCheckerListener;

#include <SofaComponentCommon/initComponentCommon.h>
#include <SofaComponentBase/initComponentBase.h>
#include <SofaComponentGeneral/initComponentGeneral.h>
#include <SofaComponentAdvanced/initComponentAdvanced.h>
#include <SofaComponentMisc/initComponentMisc.h>

#include <SofaGeneralLoader/ReadState.h>
#include <SofaValidation/CompareState.h>
#include <sofa/helper/Factory.h>
#include <sofa/helper/cast.h>
#include <sofa/helper/BackTrace.h>
#include <sofa/helper/system/FileRepository.h>
#include <sofa/helper/system/FileSystem.h>
using sofa::helper::system::FileSystem;
#include <sofa/helper/system/SetDirectory.h>
#include <sofa/helper/Utils.h>
#include <sofa/gui/GUIManager.h>
using sofa::gui::GUIManager;

#include <sofa/gui/Main.h>
#include <sofa/gui/BatchGUI.h>  // needed for BaseGUI
#include <sofa/helper/system/gl.h>
#include <sofa/helper/system/atomic.h>

using sofa::core::ExecParams ;

#include <sofa/helper/system/console.h>
using sofa::helper::Utils;

using sofa::component::misc::CompareStateCreator;
using sofa::component::misc::ReadStateActivator;
// using sofa::simulation::tree::TreeSimulation;
using sofa::simulation::graph::DAGSimulation;
using sofa::helper::system::SetDirectory;
using sofa::core::objectmodel::BaseNode ;
using sofa::gui::BaseGUI;

#include <sofa/helper/AdvancedTimer.h>
#include <sofa/helper/logging/Messaging.h>

#define BOOST_NO_CXX11_SCOPED_ENUMS
#include <boost/filesystem.hpp>
#undef BOOST_NO_CXX11_SCOPED_ENUMS

#include <sofa/gui/GuiDataRepository.h>

// see http://www.decompile.com/cpp/faq/file_and_line_error_string.htm
#define STRINGIFY(x) #x
#define TOSTRING(x) STRINGIFY(x)
#define AT __FILE__ ":" TOSTRING(__LINE__)
#define SOFA SOFA_ROOT
#define OUT_INFO(__X__) (std::cout << __X__ <<std::endl)
#define OUTT(__X__, __Y__) (std::cout << __X__ << ", " << __Y__ << std::endl)

void loadVerificationData(std::string& directory, std::string& filename, Node* node)
{
    msg_info("") << "loadVerificationData from " << directory << " and file " << filename ;

    string refFile;

    refFile += directory;
    refFile += '/';
    refFile += SetDirectory::GetFileName(filename.c_str());

    msg_info("") << "loadVerificationData " << refFile ;

    CompareStateCreator compareVisitor(ExecParams::defaultInstance());
    compareVisitor.setCreateInMapping(true);
    compareVisitor.setSceneName(refFile);
    compareVisitor.execute(node);

    ReadStateActivator v_read(ExecParams::defaultInstance(), true);
    v_read.execute(node);
}

void addGUIParameters(ArgumentParser* argumentParser)
{
    GUIManager::RegisterParameters(argumentParser);
}


int main(int argc, char** argv)
{
    auto SofaBuildPath = std::string(TOSTRING(SOFA)) + "/build";

    // OUTT("SofaBuildPath ", SofaBuildPath);
    sofa::helper::BackTrace::autodump();
    ExecParams::defaultInstance()->setAspectID(0);
    sofa::gui::initMain();

    string fileName ;
    bool noSceneCheck, temporaryFile = false;
    unsigned int nbMSSASamples = 1;
    unsigned int computationTimeSampling=0; ///< Frequency of display of the computation time statistics, in number of animation steps. 0 means never.
    string    computationTimeOutputType="stdout";
    string gui,  verif = "";
    string simulationType = "dag";

    vector<string> plugins, files;
#ifdef SOFA_SMP
    string nProcs="";
    bool        disableStealing, affinity = false;
#endif
    string colorsStatus = "unset";
    string messageHandler = "auto";
    bool enableInteraction = false ;
    int width = 600;
    int height = 600;


    ArgumentParser* argParser = new ArgumentParser(argc, argv);
    argParser->addArgument(po::value<std::vector<std::string>>(&plugins), "load,l", "load given plugins");
    argParser->addArgument(po::value<std::string>(&simulationType),  "simu,s", "select the type of simulation (bgl, dag, tree)");
    argParser->addArgument(po::value<std::string>(&verif)->default_value(""), "verification,v","load verification data for the scene");
    argParser->addArgument(po::value<std::string>(&colorsStatus)->default_value("unset", "auto")->implicit_value("yes"),"colors,c", "use colors on stdout and stderr (yes, no, auto)");
    argParser->addArgument(po::value<std::string>(&messageHandler)->default_value("auto"), "formatting,f","select the message formatting to use (auto, clang, sofa, rich, test)");
    argParser->addArgument(po::value<bool>(&enableInteraction)->default_value(false)->implicit_value(true),"interactive,i", "enable interactive mode for the GUI which includes idle and mouse events (EXPERIMENTAL)");
    argParser->addArgument(po::value<std::vector<std::string> >()->multitoken(), "argv","forward extra args to the python interpreter");

#ifdef SOFA_SMP
    argParser->addArgument(po::value<bool>(&disableStealing)->default_value(false)->implicit_value(true),           "disableStealing,w", "Disable Work Stealing")
    argParser->addArgument(po::value<std::string>(&nProcs)->default_value(""),                                      "nprocs", "Number of processor")
    argParser->addArgument(po::value<bool>(&affinity)->default_value(false)->implicit_value(true),                  "affinity", "Enable aFfinity base Work Stealing")
#endif

    addGUIParameters(argParser);
    argParser->parse();
    files = argParser->getInputFileList();
#ifdef SOFA_HAVE_DAG
    sofa::simulation::graph::init();
#endif
    sofa::component::initComponentBase();
    sofa::component::initComponentCommon();
    sofa::component::initComponentGeneral();
    sofa::component::initComponentAdvanced();
    sofa::component::initComponentMisc();

    sofa::simulation::setSimulation(new DAGSimulation());

    // Initialise paths
    sofa::gui::BaseGUI::setConfigDirectoryPath(SofaBuildPath + "/config", true);
    sofa::gui::BaseGUI::setScreenshotDirectoryPath(SetDirectory::GetCurrentDir() +  "/screenshots", true);

    if (!files.empty())
        fileName = files[0];

    for (unsigned int i=0; i<plugins.size(); i++)
      sofa::helper::system::PluginManager::getInstance().loadPlugin(plugins[i]);

    std::string defaultConfigPluginPath = sofa::helper::system::PluginRepository.getPathsJoined() + "/../patient/plugins.conf";
    std::string SofaGuiInitPath = sofa::helper::system::PluginRepository.getPathsJoined() + "/../patient/SofaGuiQt.ini";
    if (sofa::helper::system::PluginRepository.findFile(defaultConfigPluginPath, "", nullptr))
    {
        msg_info("IAB") << "Loading default plugin list in " << defaultConfigPluginPath;
        sofa::helper::system::PluginManager::getInstance().readFromIniFile(SofaGuiInitPath);
    }
    else
        msg_info("IAB") << "No plugin list found. No plugin will be automatically loaded.";

    sofa::helper::system::PluginManager::getInstance().init();

    if (int err = GUIManager::Init(argv[0],gui.c_str()))
        return err;

    if (fileName.empty())
        fileName = sofa::helper::system::DataRepository.getFile(SetDirectory::GetCurrentDir() + "/../scenes/imrt.scn");

    if (int err=GUIManager::createGUI(nullptr))
        return err;

    //To set a specific resolution for the viewer, use the component ViewerSetting in you scene graph
    GUIManager::SetDimension(width, height);

    // Create and register the SceneCheckerListener before scene loading
    if(!noSceneCheck)
        sofa::simulation::SceneLoader::addListener( SceneCheckerListener::getInstance() );

    Node::SPtr groot = sofa::simulation::getSimulation()->load(fileName.c_str());
    if( !groot )
        groot = sofa::simulation::getSimulation()->createNewGraph("");

    if (!verif.empty())
        loadVerificationData(verif, fileName, groot.get());

    sofa::simulation::getSimulation()->init(groot.get());
    GUIManager::SetScene(groot,fileName.c_str(), temporaryFile);


    //=======================================
    //Apply Options
    groot->setAnimate(true);

    if( computationTimeSampling>0 )
    {
        sofa::helper::AdvancedTimer::setEnabled("Animate", true);
        sofa::helper::AdvancedTimer::setInterval("Animate", computationTimeSampling);
        sofa::helper::AdvancedTimer::setOutputType("Animate", computationTimeOutputType);
    }

    //=======================================
    // Run the main loop
    if (int err = GUIManager::MainLoop(groot,fileName.c_str()))
        return err;
    groot = dynamic_cast<Node*>( GUIManager::CurrentSimulation() );

    if (groot!=NULL)
        sofa::simulation::getSimulation()->unload(groot);


    GUIManager::closeGUI();

    sofa::simulation::common::cleanup();
    // sofa::simulation::tree::cleanup()
    sofa::simulation::graph::cleanup();
    return 0;
}
